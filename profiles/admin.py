from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "favorite_city")
    list_filter = ("favorite_city",)
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "favorite_city",
    )
