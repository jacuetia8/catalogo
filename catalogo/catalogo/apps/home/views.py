from django.shortcuts import render_to_response
from django.template import RequestContext
from catalogo.apps.home.forms import contact_form, login_form, RegisterForm
from django.core.mail import EmailMultiAlternatives # enviamos HTML
from catalogo.apps.ventas.models import Producto
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage #paginacion
from django.contrib.auth.models import User

def base_view(request):
	return render_to_response('base.html', context_instance = RequestContext(request))

def index_view (request):	
	return render_to_response('home/index.html', context_instance = RequestContext(request))

def single_product_view(request, id_prod):
	prod = Producto.objects.get(id = id_prod)# select from producto where product.id = id_prod
	ctx = {'producto':prod}
	return render_to_response('home/single_producto.html', ctx, context_instance = RequestContext(request))

def productos_view(request, pagina):
	#int lista_prod = Producto.objects.count() # select *from Producto where status = True
	#lista_prod = Producto.objects.() # select *from Producto where status = True
	lista_prod = Producto.objects.filter(status = True) # select *from Producto where status = True
	paginator = Paginator(lista_prod, 3)
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		productos = paginator.page(page)
	except (EmptyPage, InvalidPage):
		productos = paginator.page(paginator.num_pages)
	
	ctx = {'productos':productos}
	return render_to_response('home/productos.html', ctx,context_instance = RequestContext(request))

def about_view (request):
	return render_to_response('home/about.html', context_instance = RequestContext(request))

def contacto_view (request):
	info_enviado = False #Definir  si se envio la informacion o no se envio
	email = ""
	title = ""
	text = ""
	if request.method == "POST": # evalua si el metodo fue POST
		formulario = contacto_form(request.POST) #instancia del formulario con los datos ingresados
		if formulario.is_valid(): #evalua si el formulario es valido
			info_enviado = True #la informacion se envio correctamente
			email = formulario.cleaned_data['correo'] #copia el correo ingresado en email
			title = formulario.cleaned_data['titulo'] #copia el titulo ingresado en title
			text = formulario.cleaned_data['texto'] #copia en texto ingresado en text
			''' Bloque configuracion de envio por GMAIL '''
			to_admin = 'costantinegriil@gmail.com'
			html_content = "Informacion recibida de %s <br> ---Mensaje--- <br> %s"%(email,text)
			msg = EmailMultiAlternatives('correo de contacto', html_content, 'from@server.com',[to_admin])
			msg.attach_alternative(html_content, 'text/html') #definimos el contenido como HTML
			msg.send() #enviamos el correo
			''' Fin del bloque '''
	else: #si no fue POST entonces fue el metodo GET mostrara un formulario vacio
		formulario = contact_form() #creacion del formulario vacio
	ctx = {'form':formulario, 'email' :email, "title":title, "text":text, "info_enviado":info_enviado}
	return render_to_response('home/contacto.html',ctx,context_instance = RequestContext(request))

def login_view(request):
	mensaje = ""
	if request.user.is_authenticated(): #verificamos si el usuario ya esta authenticado o logueado
		return HttpResponseRedirect('/') #si esta logueado lo dirigimos a la paguina principal
	else: # si no esta authenticado
		if request.method == "POST":
			formulario = login_form(request.POST) #creamos un objeto lo login_form
			if formulario.is_valid(): # si la informacion enviada es correcta
				usu = formulario.cleaned_data['usuario'] #guarda informacion ingresada del formulario
				pas = formulario.cleaned_data['clave'] #guarda informacion ingresada del formulario
				usuario = authenticate(username = usu, password = pas) # asigna la authenticacion del usuario
				if usuario is not None and usuario.is_active: #si el usuario es nulo y esta activo
					login(request, usuario) #se loguea al sistema con la informacion de usuario
					return HttpResponseRedirect ('/')
				else:
					mensaje = "usuario y/o clave incorrecta"
		formulario = login_form() #creamos un formulario nuevo limpio
		ctx = {'form':formulario, 'Mensaje':mensaje} # variable de contexto para pasar info a login.html
		return render_to_response('home/login.html', ctx,context_instance = RequestContext(request))

def logout_view(request):
	logout(request) #funcione django importada anterior
	return HttpResponseRedirect ('/') # rediregimos a la pagina principal

def register_view(request):
	form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			usuario = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password_one = form.cleaned_data['Password_one']
			password_two = form.cleaned_data['Password_two']
			u =User.objects.create_user(username = usuario, email = email, password = password_one)
			u.save() # guarda el objeto
			return render_to_response('home/thanks_register.html', context_instance = RequestContext(request))
		else:
			ctx = {'form':form}
			return render_to_response('home/register.html', ctx, context_instance = RequestContext(request))
	ctx = {'form':form}
	return render_to_response('home/register.html', ctx, context_instance = RequestContext(request))