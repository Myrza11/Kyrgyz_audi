import os
from register.models import CustomUser
from django.db import models
from kyrgyz_audio import settings
from gtts import gTTS
import http.client
import json
import ssl
from django.utils.text import slugify
from unidecode import unidecode
ssl._create_default_https_context = ssl._create_unverified_context
def get_tts_response(text, speaker_id, token):
    conn = http.client.HTTPSConnection("tts.ulut.kg")
    payload = json.dumps({
      "text": text,
      "speaker_id": speaker_id
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {token}'
    }
    conn.request("POST", "/api/tts", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data

text_to_convert = "Привет, как дела?"
speaker_id = "1"
access_token = "jaJ3H43CQwFr19B1WuOX2CuIK77fkHOcAUrmaRSP8yQfDtksZFwJZXFfiviY6c9x"


def save_audio_file(text, file_name):
    audio_directory = os.path.join(settings.MEDIA_ROOT, 'audio')

    if not os.path.exists(audio_directory):
        os.makedirs(audio_directory)

    tts_response = get_tts_response(text, speaker_id, access_token)
    

    audio_file_path = os.path.join(settings.MEDIA_ROOT, 'audio', file_name)
    with open(audio_file_path, 'wb') as f:
        f.write(tts_response)

    return audio_file_path

class Book(models.Model):
    pic = models.ImageField(upload_to='media/')
    name = models.CharField(max_length=128)
    short = models.TextField()
    text = models.TextField()
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    link = models.CharField(max_length=255, unique=True, editable=False)


    def split_text_into_pages(self, text):
        page_size = 3000
        words = text.split()
        pages = []
        current_page = ""
        current_length = 0

        for word in words:
            if current_length + len(word) + 1 <= page_size:
                current_page += word + " "
                current_length += len(word) + 1
            else:
                pages.append(current_page.strip())
                current_page = word + " "
                current_length = len(word) + 1

        if current_page:
            pages.append(current_page.strip())

        return pages

    def save(self, *args, **kwargs):
        if not self.link:
            transliterated_name = unidecode(self.name)
            self.link = slugify(transliterated_name)

        super().save(*args, **kwargs)

        text = self.text
        pages = self.split_text_into_pages(text)

        for index, page_text in enumerate(pages, start=1):
            page = Page.objects.create(book=self, text=page_text, page=index)
            page.save_audio()

    def __str__(self):
        return self.name


class Page(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.CharField(max_length=2000)
    page = models.IntegerField()
    audio = models.FileField(upload_to='audio/', editable=False)

    def save_audio(self):
        if not self.audio:
            audio_file_name = f"{self.book}_{self.page}.mp3"
            audio_file_path = save_audio_file(self.text, audio_file_name)
            self.audio = audio_file_path
            self.save()    

    def __str__(self):
        return f"{self.book} + {self.page}"

    class Meta:
        verbose_name_plural = "Pages"


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} + {self.book}"


class Author(models.Model):
    pic = models.ImageField(upload_to='media/')
    fullname = models.CharField(max_length=128)
    bio = models.TextField()
    link = models.CharField(max_length=255, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.link:
            transliterated_name = unidecode(self.fullname)
            self.link = slugify(transliterated_name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.fullname


class Genre(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=255, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.link:
            transliterated_name = unidecode(self.name)
            self.link = slugify(transliterated_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class User_text(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    audio_url = models.URLField()

    def __str__(self):
        return f"{self.user.username} - {self.text}"

# jaJ3H43CQwFr19B1WuOX2CuIK77fkHOcAUrmaRSP8yQfDtksZFwJZXFfiviY6c9x