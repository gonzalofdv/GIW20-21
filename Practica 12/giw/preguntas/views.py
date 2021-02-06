from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from .forms import LoginForm, PreguntaForm, RespuestaForm
from .models import Preguntas, Respuestas

# Create your views here.

@require_http_methods(["GET", "POST"])
def index(request):

	if request.method == "GET":
	    preguntas = Preguntas.objects.order_by('-fecha')
	    if request.user.is_authenticated: #Si el usuario está autenticado
	    	form = PreguntaForm()
	    	return render(request, "preguntas.html", {'preguntas': preguntas, 'pregunta_form': form})
	    #Si no está autenticado no pasamos el antivirus
	    return render(request, "preguntas.html", {'preguntas': preguntas})
	#Si el usuario está autenticado
	if request.user.is_authenticated:
		form = PreguntaForm(request.POST)
		if not form.is_valid():
			return HttpResponseBadRequest(f"Error en los datos del formulario: {form.errors}")

		titulo_f = form.cleaned_data['titulo']
		texto_f = form.cleaned_data['texto']

		pregunta = Preguntas(titulo=titulo_f, texto=texto_f, autor=request.user)
		pregunta.save()
		return redirect(reverse('preguntas:index'))

@login_required(login_url='preguntas:login')
@require_GET
def preguntafunct(request, N):
	#Muestra titulo autor fecha y texto de la pregunta de clave primaria N
	#Si tiene respuestas, muestra un listado de ellas mostrando texto autor y fecha
	#Respuestas ordenadas de nuevas a antiguas
	#Al final formulario para añadir respuesta a la pregunta
	#Si no hay pregunta con clave N, error 404

	pregunta = get_object_or_404(Preguntas, pk=N) #Error 404 si no hay pregunta

	#mostrar la pregunta y sus respuestas
	respuestas = Respuestas.objects.filter(pregunta=N)
	form = RespuestaForm()

	if respuestas is None: #Si no hay respuestas no enviamos las mismas.
		return render(request, "pregunta.html", {'pregunta': pregunta, "respuesta_form": form})

	return render(request, "pregunta.html", {'pregunta': pregunta, 'respuestas': respuestas, 'respuesta_form': form})



@login_required(login_url='preguntas:login')
@require_POST
def respuestafunct(request, N):

	form = RespuestaForm(request.POST)
	if not form.is_valid():
		return HttpResponseBadRequest(f"Error en los datos del formulario: {form.errors}")

	texto_f = form.cleaned_data['texto']

	pregunta = get_object_or_404(Preguntas, pk=N) #Error 404 si no hay pregunta

	#Creamos la respuesta para la pregunta con los datos del form
	respuesta = Respuestas.objects.create(texto=texto_f, autor=request.user, pregunta=pregunta)
	respuesta.save()

	return redirect(reverse('preguntas:pregunta', args=(N,)))


@require_http_methods(["GET", "POST"])
def loginfunct(request):
    """Muestra el formulario (GET) o recibe los datos y realiza la autenticacion (POST)"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {'login_form': form})

    # Carga el formulario desde los datos de la petición y lo valida
    form = LoginForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(f"Error en los datos del formulario: {form.errors}")

    # Toma los datos limpios del formulario
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']

    # Realiza la autenticación
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)  # Registra el usuario en la sesión
        return redirect(reverse('preguntas:index'))
    else:
        return render(request, "error.html")	


@require_GET
def logoutfunct(request):
    """Elimina al usuario de la sesión actual"""
    logout(request)  # Elimina el usuario de la sesión
    return redirect(reverse('preguntas:index'))

