from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'

class SinaLaleBakhshPhoto(TemplateView):
    template_name = 'pages/sinalalebakhsh_photo.html'


class Manifest(TemplateView):
    template_name = 'pages/manifest.html'




