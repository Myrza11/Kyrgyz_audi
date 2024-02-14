from rest_framework import serializers
from books import models


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = "__all__"
        depth = 1

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['pic'] = self.context['request'].build_absolute_uri(instance.pic.url)
        return representation



class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = "__all__"
        depth = 1

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation



class AudioField(serializers.Field):
    def to_representation(self, value):
        return self.context['request'].build_absolute_uri(value.url)

class BookSerializer(serializers.ModelSerializer):
    audio = AudioField()
    author = AuthorSerializer()
    genre = GenreSerializer()

    class Meta:
        model = models.Book
        fields = ['pic', 'name', 'short', 'link', 'author', 'genre', 'audio']
        depth = 1

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['audio'] = self.context['request'].build_absolute_uri(instance.audio.url)
        return representation
class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Page
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Favorite
        fields = "__all__"
        depth = 1




class TextSerializer(serializers.Serializer):
    text = serializers.CharField(write_only=True)

class UserTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User_text
        fields = ('user', 'text', 'audio_url')
