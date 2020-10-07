import django_filters
from django_filters import DateFilter, CharFilter, DateRangeFilter,DateFromToRangeFilter
from .models import *
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'
#INTERESTED PARTIES REGISTER
class context_ipFilter(django_filters.FilterSet):
    analysis_date=DateRangeFilter(field_name="analysis_date",label='Summary')
    #date_range = DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'YYYY/MM/DD'}))
    start_date=DateFilter(field_name="analysis_date",lookup_expr='gte',label='Start Date',widget=DateInput())
    end_date=DateFilter(field_name="analysis_date",lookup_expr='lte',label='End Date',widget=DateInput())
    #widgets={'start_date':DateInput()}
    #analysis_date = django_filters.DateFromToRangeFilter(label='Analysis Date Range',widget=DateInput())

    

    class Meta:
        model=mod9001_interestedParties
        fields=['context','status']
        #exclude=['analysis_date']
        widgets={'end_date':DateInput()}

#ISSUES REGISTER

class context_issuesFilter(django_filters.FilterSet):
    analysis_date=DateRangeFilter(field_name="analysis_date",label='Summary')
    start_date=DateFilter(field_name="analysis_date",lookup_expr='gte',label='Start Date',widget=DateInput())
    end_date=DateFilter(field_name="analysis_date",lookup_expr='lte',label='End Date',widget=DateInput())


    class Meta:
        model=mod9001_issues
        fields=['context','status']
        widgets={'end_date':DateInput()}

#REGULATORY/COMPLIANCE REQUIREMENT


class context_regulatoryFilter(django_filters.FilterSet):
    registered=DateRangeFilter(field_name="registered",label='Summary')
    start_date=DateFilter(field_name="registered",lookup_expr='gte',label='Start Date',widget=DateInput())
    end_date=DateFilter(field_name="registered",lookup_expr='lte',label='End Date',widget=DateInput())


    class Meta:
        model=mod9001_regulatoryReq
        fields=['status']
        #widgets={'end_date':DateInput()}

#############################OPPORTUNITY############


class planning_opportunityFilter(django_filters.FilterSet):
    risk_date=DateRangeFilter(field_name="risk_date",label='Summary')
    start_date=DateFilter(field_name="risk_date",lookup_expr='gte',label='Start Date',widget=DateInput())
    end_date=DateFilter(field_name="risk_date",lookup_expr='lte',label='End Date',widget=DateInput())


    class Meta:
        model=mod9001_risks
        fields=['riskrank','status','verification']
        #widgets={'end_date':DateInput()}