# forum_proj/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # your app's routes (dashboard, create issue, etc.)
    path('', include('forum_app.urls')),
    
    # built-in Django authentication (login, logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
]
