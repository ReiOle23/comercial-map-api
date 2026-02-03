from django.contrib import admin
from core.models import Business

class BusinessAdmin(admin.ModelAdmin):
    model = Business
    list_display = ("name", "iae_code", "rentability", "proximity_to_urban_center_m", "coordinates")

admin.site.register(Business, BusinessAdmin)
