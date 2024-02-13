from django.contrib import admin
from books import models

admin.site.register(models.Author)
admin.site.register(models.Genre)
admin.site.register(models.Book)
admin.site.register(models.Favorite)
admin.site.register(models.Page)

