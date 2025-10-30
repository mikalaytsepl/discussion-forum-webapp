# forum_proj/urls.py
from django.contrib import admin
from django.urls import path, include
from forum_app.views import CustomLoginView, signup 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # your app's routes (dashboard, create issue, etc.)
    path('', include('forum_app.urls')),
    
    # Our custom login overrides the default before including auth urls
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/signup/', signup, name='signup'),

    # Keep the rest of Django auth (logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
]
