"""
URL configuration for URLShortener project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include   # ← added 'include'


# ─────────────────────────────────────────────────────────────
#  This is the MAIN urls.py (the project-level one).
#  It connects to every app's urls.py using include().
#
#  include('Shortener.urls') means:
#    "Go look inside the Shortener app's urls.py for more routes"
# ─────────────────────────────────────────────────────────────

urlpatterns = [

    # Django's built-in admin panel at http://127.0.0.1:8000/admin/
    path('admin/', admin.site.urls),

    # All Shortener app URLs — '' means they start from the root /
    path('', include('Shortener.urls')),

]
