import os
import uuid
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from gtts import gTTS
from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
import requests
from rest_framework.views import APIView
from kyrgyz_audio import settings
from books import (models, serializers)
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from books.permissions import IsAdminOrReadOnly, IsOwnerOrAdminOrReadOnly


class BookAPIViewSet(viewsets.ModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
    lookup_field = 'link'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        if request.user.is_authenticated:
            user = request.user
            # Check if the book is in the user's favorites
            is_favorite = models.Favorite.objects.filter(user=user, book=instance).exists()
            serializer.data['is_favorite'] = is_favorite

        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='/my_favorites/')
    def my_favorites(self, request, *args, **kwargs):
        print('my_f')
        if request.user.is_anonymous:
            return JsonResponse({'error': 'Anonymous users cannot view favorites.'}, status=403)

        user = request.user
        # print(user)
        favorites = models.Favorite.objects.filter(user=user)
        serializer = serializers.FavoriteSerializer(favorites, many=True)

        return Response(serializer.data, status=200)

    @action(detail=True, methods=['post'])
    def create_favorite(self, request, *args, **kwargs):
        book = self.get_object()

        if request.user.is_anonymous:
            return JsonResponse({'error': 'Anonymous users cannot create favorites.'}, status=403)

        user = request.user

        if models.Favorite.objects.filter(user=user, book=book).exists():
            return JsonResponse({'error': 'Favorite already exists for this user and book.'}, status=400)

        favorite = models.Favorite.objects.create(user=user, book=book)

        serializer = serializers.FavoriteSerializer(favorite)
        return JsonResponse(serializer.data, status=201)

    @action(detail=True, methods=['delete'])
    def delete_favorite(self, request, *args, **kwargs):
        book = self.get_object()

        if request.user.is_anonymous:
            return JsonResponse({'error': 'Anonymous users cannot delete favorites.'}, status=403)

        user = request.user

        try:
            favorite = models.Favorite.objects.get(user=user, book=book)
        except models.Favorite.DoesNotExist:
            return JsonResponse({'error': 'Favorite does not exist for this user and book.'}, status=404)

        favorite.delete()

        return JsonResponse({'message': 'Favorite deleted successfully.'}, status=200)

    @action(detail=True, methods=['get'], url_path='page/(?P<page_number>\d+)/')
    def view_page(self, request, page_number, *args, **kwargs):
        book = self.get_object()
        page = get_object_or_404(models.Page, book=book, page=page_number)
        serializer = serializers.PageSerializer(page)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        author = request.data.get('author')
        genre = request.data.get('genre')

        if genre is None:
            return Response({'error': 'genre is required for creating Medicine.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if author is None:
            return Response({'error': 'author is required for creating Medicine.'},
                            status=status.HTTP_400_BAD_REQUEST)

        author = models.Author.objects.get(pk=author)
        genre = models.Genre.objects.get(pk=genre)


        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if the image field is a URL
        image_url = request.data.get('pic')
        if image_url:
            # Download the image and save it as a temporary file
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(requests.get(image_url).content)
            img_temp.flush()

            # Save the temporary file to the image field
            serializer.validated_data['pic'] = File(img_temp)

            # Adding author and genre instances to the serializer data before saving
        serializer.validated_data['genre'] = genre
        serializer.validated_data['author'] = author

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GenresAPIViewSet(viewsets.ModelViewSet):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    lookup_field = 'link'
    permission_classes = [IsAdminOrReadOnly]
    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('link')
        if pk:
            books = models.Book.objects.filter(genre__link=pk)
            serializer = serializers.BookSerializer(books, many=True)
            return Response({'books': serializer.data})
        else:
            return Response({'error': 'No pk provided'})

class AuthorsAPIViewSet(viewsets.ModelViewSet):
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    lookup_field = 'link'
    permission_classes = [IsAdminOrReadOnly]
    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('link')
        if pk:
            books = models.Book.objects.filter(author__link=pk)
            serializer = serializers.BookSerializer(books, many=True)
            return Response({'books': serializer.data})
        else:
            return Response({'error': 'No pk provided'})


def save_audio_file(text, file_name):
    audio_directory = os.path.join(settings.MEDIA_ROOT, 'audio')

    if not os.path.exists(audio_directory):
        os.makedirs(audio_directory)

    audio_file_path = os.path.join(audio_directory, file_name)

    tts = gTTS(text, lang='ru')
    tts.save(audio_file_path)

    return audio_file_path

class UserTextListView(generics.ListAPIView):
    serializer_class = serializers.UserTextSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return models.User_text.objects.filter(user=user)

class UserTextDetailView(generics.RetrieveAPIView):
    queryset = models.User_text.objects.all()
    serializer_class = serializers.UserTextSerializer
    lookup_field = 'pk'
    permission_classes = [IsOwnerOrAdminOrReadOnly]

class GPTResponseApiView(APIView):
    serializer_class = serializers.TextSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        chat_records = models.User_text.objects.filter(user=request.user)
        chat_records_serializer = serializers.UserTextSerializer(chat_records, many=True)
        return Response(chat_records_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = serializers.TextSerializer(data=request.data)

        if serializer.is_valid():
            input_text = serializer.validated_data['text']

            file_name = f'{uuid.uuid4()}.mp3'
            audio_file_path = save_audio_file(input_text, file_name)

            audio_url = os.path.join(settings.MEDIA_URL, 'audio', file_name)

            chat_record = models.User_text.objects.create(
                user=request.user,
                text=input_text,
                audio_url=audio_url
            )

            chat_record_serializer = serializers.UserTextSerializer(chat_record)

            response_data = {
                'text': input_text,
                'audio_url': audio_url,
                'chat_record': chat_record_serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# "email": "davletazimov142@gmail.com",