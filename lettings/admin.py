from django.contrib import admin
from .models import Address, Letting


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("number", "street", "city", "state", "zip_code", "country_iso_code")
    list_filter = ("state", "city", "country_iso_code")
    search_fields = ("street", "city")


@admin.register(Letting)
class LettingAdmin(admin.ModelAdmin):
    list_display = ("title", "address")
    search_fields = ("title", "address__street", "address__city")
