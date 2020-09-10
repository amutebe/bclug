
from django.contrib import admin
from django.urls import path, include




urlpatterns = [
    path('msem/', admin.site.urls),
    path('',include('accounts.urls'))
  
]
