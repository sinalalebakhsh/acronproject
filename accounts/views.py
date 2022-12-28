from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect


from .forms import CustomUserCreationForm, CustomUserChangeForm


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

def redirect_to_home_customize(request):
    return redirect(reverse('home'))

