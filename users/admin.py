from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('email', 'is_staff', 'is_active', 'phone_number', 'country')
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'avatar', 'country')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
