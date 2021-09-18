from django.contrib import admin
from .models import Content, Entry, Photo, Platform

# Register your models here.
admin.site.register(Content)
admin.site.register(Entry)
admin.site.register(Platform)
admin.site.register(Photo)