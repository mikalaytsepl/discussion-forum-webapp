# forum_proj/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from forum_app.views import signup

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # your app's routes (dashboard, create issue, etc.)
    path('', include('forum_app.urls')),
    
    # Our custom pages (order matters: put these BEFORE the auth include)
    path('accounts/login/', LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),

    path('accounts/signup/', signup, name='signup'),

    # Keep the rest (logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
]
