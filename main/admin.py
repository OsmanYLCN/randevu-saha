from django.contrib import admin
from .models import CustomUser, Halisaha, Reservation
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ("Kullanıcı Tipi", {'fields': ('user_type',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Halisaha)
admin.site.register(Reservation)