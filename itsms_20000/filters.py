import django_filters
from django_filters import DateFilter, CharFilter, DateRangeFilter,DateFromToRangeFilter
from .models import *
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class serviceRequestFilter(django_filters.FilterSet):
    request_date=DateRangeFilter(field_name="date",label='Summary')
    start=DateFilter(field_name="date",lookup_expr='gte',label='Start Date',widget=DateInput())
    end=DateFilter(field_name="date",lookup_expr='lte',label='End Date',widget=DateInput())
    


    class Meta:
        model=mod20000_service_request
        fields=['request_type','request_mode','IT_service','priority']