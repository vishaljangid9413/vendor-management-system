from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'is_active', 'is_staff', 'is_superuser', 'is_deleted')
    search_fields = ('name', 'vendor_code', )