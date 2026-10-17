from django.contrib import admin

from .models import ShortenedURL


# Register ShortenedURL so we can view/manage it
# at http://127.0.0.1:8000/admin/
admin.site.register(ShortenedURL)
