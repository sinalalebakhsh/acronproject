from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 

from .forms import CustomUserCreationForm
from .forms import UserChangeForm

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = UserChangeForm
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('age',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)




