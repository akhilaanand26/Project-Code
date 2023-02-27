from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import User
from .forms import UserChangeForm, SignupForm

# Register your models here.

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = SignupForm

    list_display = ('email', 'first_name', 'last_name', 'role', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role', 'profile_pic')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name','email', 'role', 'password1', 'password2'),
        }),
    )
    search_fields = ('email','first_name',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)