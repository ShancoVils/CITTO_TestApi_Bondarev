from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email','FIO','Official','is_staff', 'is_active','activate_code')
    list_filter = ('email', 'is_staff', 'is_active','activate_code')
    fieldsets = (
        (None, {'fields': ('email','FIO','Official','password','activate_code')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','FIO','Official', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email','name',)
    ordering = ('email','name',)
admin.site.register(CustomUser, CustomUserAdmin)