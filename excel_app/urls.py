# django_excel/urls.py 
from django.contrib import admin
from django.urls import path

from excel_app import views

urlpatterns = [
#    path('admin/', admin.site.urls),
    #path('', views.ExcelPageView.as_view(), name='home'), 
    path('excel/', views.export_users_xls, name='export_excel'),
    path('excel-styling/', views.export_styling_xls, name='export_styling_excel'),
    path('export-write-xls/', views.export_write_xls, name='export_write_xls'),
]