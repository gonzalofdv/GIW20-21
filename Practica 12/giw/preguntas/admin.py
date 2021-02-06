from django.contrib import admin

# Register your models here.

from .models import Preguntas, Respuestas

admin.site.register(Preguntas)
admin.site.register(Respuestas)