from django.shortcuts import render_to_response
from django.template import RequestContext
from catalogo.apps.ventas.forms import add_Product_form, add_Categori_form, add_Marc_form
from catalogo.apps.ventas.models import Producto, Categoria, Marca
from django.http import HttpResponseRedirect

def add_product_view (request):
	info = "inicializado"
	if request.method == "POST":
		formulario = add_Product_form(request.POST, request.FILES)
		if formulario.is_valid():
			add = formulario.save(commit = False)
			add.status = True
			add.save() # guarda la informacion
			formulario.save_m2m() # guarda las relaciones ManyToMany
			info = "Guardado Satisfactoriamente"
			return HttpResponseRedirect ('/') #('/Producto/%s' %add.id)
	else:
		formulario = add_Product_form()
	ctx = {'form':formulario, 'informacion':info}
	return render_to_response('ventas/add_producto.html', ctx,context_instance = RequestContext(request))# Create your views here.

def add_categori_view (request):
	info = "inicializado"
	if request.method == "POST":
		formulario = add_Categori_form(request.POST, request.FILES)
		if formulario.is_valid():
			add = formulario.save(commit = False)
			#add.status = True
			add.save() # guarda la informacion
			#formulario.save_m2m() # guarda las relaciones ManyToMany
			info = "Guardado Satisfactoriamente"
			return HttpResponseRedirect ('/') #('/Producto/%s' %add.id)
	else:
		formulario = add_Categori_form()
	ctx = {'form':formulario, 'informacion':info}
	return render_to_response('ventas/add_categoria.html', ctx,context_instance = RequestContext(request))# Create your views here.

def add_marc_view (request):
	info = "inicializado"
	if request.method == "POST":
		formulario = add_Marc_form(request.POST, request.FILES)
		if formulario.is_valid():
			add = formulario.save(commit = False)
			#add.status = True
			add.save() # guarda la informacion
			#formulario.save_m2m() # guarda las relaciones ManyToMany
			info = "Guardado Satisfactoriamente"
			return HttpResponseRedirect ('/') #('/Producto/%s' %add.id)
	else:
		formulario = add_Marc_form()
	ctx = {'form':formulario, 'informacion':info}
	return render_to_response('ventas/add_marca.html', ctx,context_instance = RequestContext(request))# Create your views here.

def edit_product_view (request, id_prod):
	info = ""
	prod = Producto.objects.get(pk = id_prod)
	if request.method == "POST":
		formulario = add_Product_form(request.POST, request.FILES, instance = prod)
		if formulario.is_valid():
			edit_prod = formulario.save(commit = False)
			formulario.save_m2m() # guarda las relaciones ManyToMany
			edit_prod.status = True
			edit_prod.save() # guarda la informacion
			info = "Guardado Satisfactoriamente"
			return HttpResponseRedirect ('/') #('/Producto/%s' % edit_prod.id)
	else:
		formulario = add_Product_form(instance = prod)
	ctx = {'form':formulario, 'informacion':info}
	return render_to_response('ventas/edit_producto.html', ctx,context_instance = RequestContext(request))# Create your views here.

def del_product_view (request, id_prod):
	info = "inicializado"
	try:
		prod = Producto.objects.get(pk = id_prod)
		prod.delete() # elimina la informacion
		info = "Producto Eliminado Correctamente"
		return HttpResponseRedirect ('/productos/page/1') #('/Producto/%s' % edit_prod.id)
	except:
		info = "Producto no se puede Eliminar"
		# return render_to_response('ventas/edit_producto.html', ctx,context_instance = RequestContext(request))# Create your views here.
		return HttpResponseRedirect ('/productos/page/1') #('/Producto/%s' % edit_prod.id)
