from django.contrib import admin
from .models import Profile, Background

admin.site.register(Profile)

@admin.register(Background)
class BackgroundAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Image', {
            'fields':('name', 'image'),
            'description': '<h3>Rozmiar - 960 x 540</h3>',
            }
        ),
    ]