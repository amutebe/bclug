
from django.contrib import admin
from django.urls import path, include




urlpatterns = [
    path('msem/', admin.site.urls),
#    path('admin/defender/', include('defender.urls')),

    path('',include('accounts.urls')),
    
    
    
  
]
