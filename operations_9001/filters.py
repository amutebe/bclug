import django_filters
from django_filters import DateFilter, CharFilter, DateRangeFilter,DateFromToRangeFilter

from .models import *
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date' 

#######################TRAINING REGISTER#############
class trainingRegFilter(django_filters.FilterSet):
    train_date=DateRangeFilter(field_name="train_date",label='Summary')
    start=DateFilter(field_name="train_date",lookup_expr='gte',label='Start Date',widget=DateInput())
    end=DateFilter(field_name="train_date",lookup_expr='lte',label='End Date',widget=DateInput())

    class Meta:
        model=mod9001_trainingregister
        fields=['decision','trainee']
        #widgets={'end_date':DateInput()} 

########################QMS PLANNER ##################################
class planning_qmsFilter(django_filters.FilterSet):
    plan_date=DateRangeFilter(field_name="plan_date",label='Summary')
    start=DateFilter(field_name="plan_date",lookup_expr='gte',label='Start Date',widget=DateInput())
    end=DateFilter(field_name="plan_date",lookup_expr='lte',label='End Date',widget=DateInput())
 


    class Meta:
        model=mod9001_qmsplanner
        fields=['status','qmsstatus']
        #widgets={'end_date':DateInput()}
######################## PROVIDER ASSESSSMENT ##################################
class providerAssessmentFilter(django_filters.FilterSet):
    assesment_date=DateRangeFilter(field_name="start",label='Summary')
    start=DateFilter(field_name="start",lookup_expr='gte',label='Start Date',widget=DateInput())
    end=DateFilter(field_name="start",lookup_expr='lte',label='End Date',widget=DateInput())
 


    class Meta:
        model=mod9001_providerassessment
        fields=['Provider','qmsstatus']
        #widgets={'end_date':DateInput()}
 ###################DOCUMENT MANAGER###########################
class documentmanagerFilter(django_filters.FilterSet):
    class Meta:
        model=mod9001_document_manager
        fields=['doc_name','doc_type','standard','status']
        #widgets={'end_date':DateInput()}
    
########################TRAINING PLANNER#######################
class planning_trainingplannerFilter(django_filters.FilterSet):
    trainng_date=DateRangeFilter(field_name="trainng_date",label='Summary')
    start=DateFilter(field_name="trainng_date",lookup_expr='gte',label='Start Date',widget=DateInput())
    end=DateFilter(field_name="trainng_date",lookup_expr='lte',label='End Date',widget=DateInput())
    


    class Meta:
        model=mod9001_trainingplanner
        fields=['type','status','trainplannerstatus']
        #widgets={'end_date':DateInput()}

########################INCIDENT REGISTER#######################
class Operations_incidentRegisterFilter(django_filters.FilterSet):
    incident_date=DateRangeFilter(field_name="date_today",label='Summary')
    start=DateFilter(field_name="date",lookup_expr='gte',label='Start Date',widget=DateInput())
    end=DateFilter(field_name="date",lookup_expr='lte',label='End Date',widget=DateInput())
    


    class Meta:
        model=mod9001_incidentregisterStaff
        fields=['classification']