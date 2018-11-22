from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from .forms import UserCreationForm, UserChangeForm
from .models import User
# Register your models here.

class UserAdmin(BaseUserAdmin) : 
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'get_full_name',
        'email',
        'nickname',
        'is_active',
        'is_superuser',
        'date_joined',
    )
    list_display_links = (
        'get_full_name',
    )
    list_filter = (
        'is_superuser',
        'is_active',
    )
    fieldsets = (
        (None, {'fields': ('email','password')}),
        (_('Personal info'), {'fields': ('nickname',)}),
        (_('social'),{'fields':('followers','following')}),
        (_('Permissions'),{'fields': ('is_active','is_superuser',)}),
    )
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('email', 'nickname','password1', 'password2')
        }),
    )
    search_fields = ('email','nickname')
    ordering = ('-date_joined',)
    filter_horizontal = ()

#Now register the new UserAdmin...
admin.site.register(User, UserAdmin)