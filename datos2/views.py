from abm.funciones import *
from models import *
from forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Q
from django.forms.models import modelformset_factory
from stronghold.decorators import public
from django.contrib.auth.decorators import permission_required

nombresFormularios={unicode("persona"):PersonaForm,
					unicode("telefono"):TelefonoForm,
					unicode("domicilio"):DomicilioForm}
					
nombresModelos={unicode("persona"):Persona,
				unicode("telefono"):Telefono,
				unicode("domicilio"):Domicilio}



def alta_persona(request):
	if request.user.has_perm('datos.add_'+modelo):
		DomicilioFormSet=modelformset_factory(Domicilio, extra=10, exclude=('persona','observacion',))	
		#TelefonoFormSet=modelformset_factory(Telefono, extra=1, exclude=('persona','observacion',))	
		if request.method=='POST':
			formulario1=PersonaForm(request.POST)			
			formulario2=DomicilioFormSet(request.POST, queryset=Domicilio.objects.none(),prefix='domicilios',initial=[{'tipo_domicilio': u'legal','direccion': u'hola','localidad': u'rawson'}])
			#formulario3=TelefonoFormSet(request.POST, queryset=Domicilio.objects.none(),prefix='telefonos',)
			if (formulario1.is_valid() and formulario2.is_valid()):
				domicilios=formulario2.save(commit=False)
				#telefonos=formulario3.save(commit=False)
				persona=formulario1.save()				
				
				for domicilio in domicilios:
					domicilio.persona=persona
					domicilio.save()
				"""	
				for telefono in telefonos:
					telefono.persona=persona
					telefono.save()
				"""
					
				return HttpResponseRedirect('/datos2/lista/persona')
		else:
			formulario1=PersonaForm()
			formulario2=DomicilioFormSet(queryset=Domicilio.objects.none(),prefix='domicilios',initial=[{'tipo_domicilio': u'legal','direccion': u'hola','localidad': u'rawson'}])
			#formulario3=TelefonoFormSet(queryset=Domicilio.objects.none(),prefix='telefonos',)			
		return render_to_response('formulario_personas.html', {'formulario': formulario1, 'formulario2': formulario2, 'nombre': Persona._meta.verbose_name_plural, 'n': Persona._meta.verbose_name,}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/403')
		

def alta_(request, modelo):
	if request.user.has_perm('datos.add_'+modelo):
		return alta(request,nombresModelos[modelo],nombresFormularios[modelo],"datos2",'formulario_datos2.html')
	else:
		return HttpResponseRedirect('/403')
		
def lista_(request,modelo):
	return lista(request,nombresModelos[modelo],'lista_datos2.html')

	
def editar_(request, modelo, id_profesion):
	if request.user.has_perm('datos.change_'+modelo):
		return editar(request, id_profesion, nombresModelos[modelo], nombresFormularios[modelo],"datos2",'formulario_datos2.html') 
	else:
		return HttpResponseRedirect('/403')
		
def eliminar_(request, modelo, id_domicilio):
	if request.user.has_perm('datos.delete_'+modelo):
		return eliminar(request,  nombresModelos[modelo], id_domicilio,"datos2")
	else:
		return HttpResponseRedirect('/403')
		

