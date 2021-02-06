from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

#urlpatterns = [
#path('',views.home),
#path('product/',views.product),
#path('customer/<str:name>',views.customer) 
#]

urlpatterns = [
    path('',include('excel_app.urls')),
    path('',include('issues_9001.urls')),
    path('',include('operations_9001.urls')),
    path('', views.home, name="home"),
    path('product/', views.product, name='product'),
    path('customer/<str:pk_test>/', views.customer, name="customer"),
    path('create_order/',views.createorder,name="createorder"),
    path('update_order/<str:pk_test>/',views.updateorder,name="updateorder"),
    path('edit_car/<str:pk_test>/',views.edit_car,name="edit_car"),
    path('car_editing/',views.car_editing,name="car_editing"),
    path('approve_car/<str:pk_test>/',views.approve_car,name="approve_car"),
    path('verify_car/<str:pk_test>/',views.verify_car,name="verify_car"),
    path('cars_view/',views.cars_view,name="cars_view"),
    path('cars_7daysToExpiryview/<str:pk_test>/',views.cars_7daysToExpiryview,name="cars_7daysToExpiryview"),
    path('cars_pending/',views.cars_pending,name="cars_pending"), 
    path('cars_7daystoEpirepending/',views.cars_7daystoEpirepending,name="cars_7daystoEpirepending"), 
    path('cars_due/',views.cars_due,name="cars_due"), 
    path('delete_order/<str:pk_test>/',views.deleteorder,name="deleteorder"),
    path('delete_car/<str:pk_test>/',views.deletecar,name="deletecar"),
    path('register/',views.register,name="register"),
    path('login/',views.loginpage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('createCAR/',views.createCAR,name="createCAR"),
    path('createCARs/',views.createCARs,name="createCARs"),
    path('CARerror/',views.CARerror,name="CARerror"),
    path('SaveCAR/',views.SaveCAR,name="SaveCAR"),
    path('hideshow/',views.hideshow,name="hideshow"),
    path('ticket_class_view_3/',views.ticket_class_view_3,name="ticket_class_view_3"),
  
    
    
]
admin.site.site_title = 'My site admin'
admin.site.site_header = "MSEM Login"
admin.site.site_title = "MSEM Admin Portal"
admin.site.index_title = "Welcome to MSEM System"