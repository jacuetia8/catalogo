from catalogo.apps.ventas.models import Producto, Categoria, Marca
from django import forms

class add_Product_form(forms.ModelForm):
	class Meta:
		model = Producto
		#se escluye el status por que en el modelo lo ponemos default=True
		exclude = {'status',}
		
class add_Categori_form(forms.ModelForm):
	class Meta:
		model = Categoria
		#se escluye el status por que en el modelo lo ponemos default=True
		exclude = {'status',}

class add_Marc_form(forms.ModelForm):
	class Meta:
		model = Marca
		#se escluye el status por que en el modelo lo ponemos default=True
		exclude = {'status',}

