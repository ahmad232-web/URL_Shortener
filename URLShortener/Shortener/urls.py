from django.urls import path

from . import views   # import views from THIS app (Shortener)


# ────────────────────────────────────────────────────────────
#  URL patterns for the Shortener app
#
#  path('', views.home, name='home')
#    → When user visits  http://127.0.0.1:8000/
#      Django calls the  home()  function in views.py
#
#  path('go/<str:short_code>/', views.redirect_to_original, name='redirect')
#    → When user visits  http://127.0.0.1:8000/go/aB3xZ1/
#      Django calls the  redirect_to_original()  function
#      and passes "aB3xZ1" as the  short_code  variable
# ────────────────────────────────────────────────────────────

urlpatterns = [

    # Home page — shows the form and history table
    path('', views.home, name='home'),

    # Redirect page — <str:short_code> captures the code from the URL
    path('go/<str:short_code>/', views.redirect_to_original, name='redirect'),

]
