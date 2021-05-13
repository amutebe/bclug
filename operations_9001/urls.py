from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path('dateValidation/', views.dateValidation, name='dateValidation'),
path('doc_manager/', views.doc_manager, name='doc_manager'),
path('documentmanager_report/',views.documentmanager_report,name="documentmanager_report"),
path('calibration/', views.cali, name='calibration'),
path('maintenance/', views.maintenance, name='maintenance'),
path('qms_planner/', views.qms_planner, name='qms_planner'),
path('qms_report/',views.qms_report,name="qms_report"),
path('qms_pending/', views.qms_pending, name='qms_pending'),
path('approve_qms/<str:pk_test>/',views.approve_qms,name="approve_qms"),
path('verify_qms/<str:pk_test>/',views.verify_qms,name="verify_qms"),
path('qms_due/',views.qms_due,name="qms_due"),
path('qms_7daysToExpiryview/<str:pk_test>/',views.qms_7daysToExpiryview,name="qms_7daysToExpiryview"),
path('trainingReg/', views.trainingReg, name='trainingReg'),
path('training_register_report/',views.training_register_report,name="training_register_report"),
path('Verify_trainingregister/<str:pk_test>/',views.Verify_trainingregister,name="Verify_trainingregister"),
path('trainingregister_due/',views.trainingregister_due,name="trainingregister_due"),
path('trainingregister_7daysToExpiryview/<str:pk_test>/',views.trainingregister_7daysToExpiryview,name="trainingregister_7daysToExpiryview"),

path('training_planner/', views.training_planner, name='training_planner'),
path('trainingplan_report/',views.trainingplan_report,name="trainingplan_report"),

path('trainplanner_pending/', views.trainplanner_pending, name='trainplanner_pending'),
path('approve_trainplanner/<str:pk_test>/',views.approve_trainplanner,name="approve_trainplanner"),
path('training_due/',views.training_due,name="training_due"),
path('verify_training/<str:pk_test>/',views.verify_training,name="verify_training"),
path('training_7daysToExpiryview/<str:pk_test>/',views.training_7daysToExpiryview,name="training_7daysToExpiryview"),

path('incidentRegister/', views.incidentRegister, name='incidentRegister'),
path('incident_report/', views.incident_report, name='incident_report'),
path('incident_log_report/', views.incident_log_report, name='incident_log_report'),
path('ajax/load_description/', views.load_description, name='ajax_load_description'),
path('ajax/load_process/', views.load_process, name='ajax_load_process'),


path('customerRegister/', views.customerRegister, name='customerRegister'),
path('incidentRegisterStaff/', views.incidentRegisterStaff, name='incidentRegisterStaff'),
path('Verify_incidentregister/<str:pk_test>/',views.Verify_incidentregister,name="Verify_incidentregister"),
path('incidentregister_due/',views.incidentregister_due,name="incidentregister_due"),
path('incidentregister_7daysToExpiryview/<str:pk_test>/',views.incidentregister_7daysToExpiryview,name="incidentregister_7daysToExpiryview"),


path('correctiveaction/', views.correctiveaction, name='correctiveaction'),
path('correctiveaction_report/', views.correctiveaction_report, name='correctiveaction_report'),
path('correctiveactionRequest_report/', views.correctiveactionRequest_report, name='correctiveactionRequest_report'),



path('planning/', views.planning, name='planning'),
path('planning_pending/', views.planning_pending, name='planning_pending'),
path('approve_planning/<str:pk_test>/',views.approve_planning,name="approve_planning"),
path('planning_due/',views.planning_due,name="planning_due"), 
path('planning_7daysToExpiryview/<str:pk_test>/',views.planning_7daysToExpiryview,name="planning_7daysToExpiryview"),
path('verify_planning/<str:pk_test>/',views.verify_planning,name="verify_planning"),

path('changerequest/', views.changerequest, name='changerequest'),
path('changerequest_pending/', views.changerequest_pending, name='changerequest_pending'),
path('approve_changerequest/<str:pk_test>/',views.approve_changerequest,name="approve_changerequest"),
path('changerequest_due/',views.changerequest_due,name="changerequest_due"), 
path('changerequest_7daysToExpiryview/<str:pk_test>/',views.changerequest_7daysToExpiryview,name="changerequest_7daysToExpiryview"),
path('changeRegister_report/', views.changeRegister_report, name='changeRegister_report'),


path('verify_changerequest/<str:pk_test>/',views.verify_changerequest,name="verify_changerequest"),

path('customercomplaint/', views.customercomplaint, name='customercomplaint'),
path('customer_complaint_report/', views.customer_complaint_report, name='customer_complaint_report'),


path('customercomplaint_due/',views.customercomplaint_due,name="customercomplaint_due"), 
path('customercomplaint_7daysToExpiryview/<str:pk_test>/',views.customercomplaint_7daysToExpiryview,name="customercomplaint_7daysToExpiryview"),
path('Verify_customercomplaint/<str:pk_test>/',views.Verify_customercomplaint,name="Verify_customercomplaint"),

path('providerassessment/', views.providerassessment, name='providerassessment'),
path('providerAssessment_report/', views.providerAssessment_report, name='providerAssessment_report'),

#path('qms_pending/', views.qms_pending, name='qms_pending'),
path('approve_qms/<str:pk_test>/',views.approve_qms,name="approve_qms"),
path('Verify_providerassessments/<str:pk_test>/',views.Verify_providerassessments,name="Verify_providerassessments"),
path('providerassessments_due/',views.providerassessments_due,name="providerassessments_due"),
path('providerassesment_7daysToExpiryview/<str:pk_test>/',views.providerassesment_7daysToExpiryview,name="providerassesment_7daysToExpiryview"),

path('customersatisfaction/', views.customersatisfaction, name='customersatisfaction'),
path('customersatisfaction_report/', views.customersatisfaction_report, name='customersatisfaction_report'),



path('Verify_customersatisfaction/<str:pk_test>/',views.Verify_customersatisfaction,name="Verify_customersatisfaction"),
path('customersatisfaction_due/',views.customersatisfaction_due,name="customersatisfaction_due"),
path('customersatisfaction_7daysToExpiryview/<str:pk_test>/',views.customersatisfaction_7daysToExpiryview,name="customersatisfaction_7daysToExpiryview"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)