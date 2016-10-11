#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
#from django.core.context_processors import csrf
from django.template.context_processors import csrf
from usuario.forms import MyRegistrationForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import HttpResponse
from django.forms import ModelForm
from django.contrib import auth
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from .models import *



'''
Función que valida si un usuario está autenticado, si no está autenticado
se muestra el formulario del login.
'''
def Login(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('index')
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                #if acceso.is_staff:
                    login(request, acceso)
                    return HttpResponseRedirect('index')
                else:
                    return render_to_response('usuario/user_inactive.html', context_instance=RequestContext(request))
            else:
                return render_to_response('usuario/not_user.html', context_instance=RequestContext(request))
    else:
        form = AuthenticationForm()
    return render_to_response('usuario/login.html',{'form':form}, context_instance=RequestContext(request))



'''
Función que permite crear usuarios, si la cuenta se creo con éxito
se redirige a otro template.
'''
def Create_User(request):
    usuario = request.user
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            nuevo_usuario = form.save()
            return HttpResponseRedirect('user_success')
        else:
            return HttpResponseRedirect('index')
    args = {}
    args['form'] = MyRegistrationForm()
    return render(request, 'usuario/create_user.html', args)



'''
Vista de la plantilla que se muestra cuando la cuenta de usuario se creó correctamente.
'''
def User_Success(request):
    usuario = request.user
    return render_to_response('usuario/user_success.html', {'usuario':usuario}, context_instance=RequestContext(request))



'''
Vista de la plantilla principal, accede a esta luego de iniciar sesión.
'''
@login_required(login_url='login')
def Index(request):
    usuario = request.user
    return render_to_response('usuario/index.html', {'usuario':usuario}, context_instance=RequestContext(request))



'''
Funcion que cierra la sesión del usuario.
'''
@login_required(login_url='login')
def Logout(request):
    logout(request)
    return HttpResponseRedirect('index')



'''
Vista de la plantilla que muestra el perfil del usuario autenticado.
'''
@login_required(login_url='login')
def Profile(request):
    user = request.user
    return render_to_response('usuario/profile.html', {'user':user}, context_instance=RequestContext(request))



'''
Vista de la plantilla que se muestra el formulario para cambiar la contraseña del usuario logeado.
'''
@login_required(login_url='login')
def Change_Password(request):
    user = request.user
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            print "PASSWORD CHANGEEEEEEE"
            return HttpResponseRedirect('index')
        else:
            print "ERROR PASSWORD CHANGEEEEEEE"
            return HttpResponseRedirect('change_password')
    return render(request, 'usuario/change_password.html', {'form': form})