from django.shortcuts import render, redirect
from django.urls import reverse,reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from app_blog.models import Posteo

# Create your views here.

class PosteoListView(LoginRequiredMixin,ListView):
   model = Posteo
   template_name = 'app_blog/lista_posteos.html'

class PosteoCreateView(LoginRequiredMixin,CreateView):
   model = Posteo
   fields = ('titulo', 'bajada', 'creador', 'imagen', 'texto','fecha_publicacion' )
   success_url = reverse_lazy('lista_posteos')

class PosteoDetailView(LoginRequiredMixin,DetailView):
   model = Posteo
   success_url = reverse_lazy('lista_posteos')

class PosteoUpdateView(LoginRequiredMixin,UpdateView):
   model = Posteo
   fields = ('titulo', 'bajada', 'creador', 'imagen', 'texto', 'fecha_publicacion' )
   success_url = reverse_lazy('lista_posteos')

class PosteoDeleteView(LoginRequiredMixin,DeleteView):
   model = Posteo
   success_url = reverse_lazy('lista_posteos')


