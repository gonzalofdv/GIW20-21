from django.urls import path

from . import views

# Imprescindible dar un nombre para crear un namespace y poder referirse a estas rutas como
# opiniones:index, opiniones:login, etc.
app_name = "preguntas"

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:N>', views.preguntafunct, name='pregunta'),
    path('login', views.loginfunct, name='login'),
    path('logout', views.logoutfunct, name='logout'),
    path('<int:N>/respuesta', views.respuestafunct, name='respuesta'),
]