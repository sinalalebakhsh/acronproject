from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Metta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('age', )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields







