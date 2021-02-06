from django.db import models
from django.conf import settings
from django.utils.html import escape

# Create your models here.

class Preguntas(models.Model):
	N = models.AutoField(primary_key=True)
	titulo = models.CharField(max_length=250)
	texto = models.CharField(max_length=5000)
	fecha = models.DateTimeField(auto_now_add=True)
	autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	def clean(self):
		#Escapamos el texto por si contiene caracteres HTML
		self.texto = escape(self.texto)
		self.titulo = escape(self.titulo)

	def num_respuestas(self):
		num = Respuestas.objects.filter(pregunta = self).count()
		return num

class Respuestas(models.Model):
	texto = models.CharField(max_length=5000)
	fecha = models.DateTimeField(auto_now_add=True)
	autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	pregunta = models.ForeignKey(Preguntas, on_delete=models.CASCADE)

	def clean(self):
		self.texto = escape(self.texto)