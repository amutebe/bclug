import django_filters
from django_filters import DateFilter, CharFilter, DateRangeFilter,DateFromToRangeFilter

from .models import *
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date' 
########################QMS PLANNER ##################################
class planning_qmsFilter(django_filters.FilterSet):
    plan_date=DateRangeFilter(field_name="plan_date",label='Summary')
    start=DateFilter(field_name="plan_date",lookup_expr='gte',label='Start Date',widget=DateInput())
    end=DateFilter(field_name="plan_date",lookup_expr='lte',label='End Date',widget=DateInput())
 


    class Meta:
        model=mod9001_qmsplanner
        fields=['status','qmsstatus']
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