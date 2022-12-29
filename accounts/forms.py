from django.contrib.auth.forms import UserCreationForm, UserChangeForm


from .models import CustomUser




class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', )
        # fields = UserCreationForm.Meta.fields


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', )
        # fields = UserCreationForm.Meta.fields



