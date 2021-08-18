import django_filters
from django_filters import DateFilter, CharFilter, DateRangeFilter,DateFromToRangeFilter
from .models import *
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class serviceRequestFilter(django_filters.FilterSet):
    request_date=DateRangeFilter(field_name="planning_date",label='Summary')
    start=DateFilter(field_name="planning_date",lookup_expr='gte',label='Start Date',widget=DateInput())
    end=DateFilter(field_name="planning_date",lookup_expr='lte',label='End Date',widget=DateInput())
    error = django_filters.CharFilter(lookup_expr='icontains', distinct=True)
    solution = django_filters.CharFilter(lookup_expr='icontains', distinct=True)
    #assigned = django_filters.CharFilter(lookup_expr='icontains', distinct=True)


    class Meta:
        model=mod20000_service_planning
        fields=['service_category','component_affected','error','solution','assigned']