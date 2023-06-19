from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'pk')
