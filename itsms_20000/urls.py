from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
path('services_request/', views.services_request, name='services_request'),
path('service_request_report/', views.service_request_report, name='service_request_report'),
path('serviceRequestPlanning/<str:sr_id>/', views.serviceRequestPlanning, name='serviceRequestPlanning'),
path('Verify_service_request/<str:pk_test> <str:planning_date>/', views.Verify_service_request, name="Verify_service_request"),
path('serviceRequest_due/', views.serviceRequest_due, name="serviceRequest_due"),
path('serviceRequest_rejected/', views.serviceRequest_rejected, name="serviceRequest_rejected"),
path('serviceRequest_7daysToExpiryview/<str:pk_test>/', views.serviceRequest_7daysToExpiryview, name="serviceRequest_7daysToExpiryview"),
path('serviceRequest_pending_planning/', views.serviceRequest_pending_planning, name="serviceRequest_pending_planning"),


]