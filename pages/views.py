from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

class SinaLaleBakhshPhoto(LoginRequiredMixin, TemplateView):
    template_name = 'pages/sinalalebakhsh_photo.html'


class Manifest(LoginRequiredMixin, TemplateView):
    template_name = 'pages/manifest.html'




