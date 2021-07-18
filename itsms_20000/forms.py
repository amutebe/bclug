from django.forms import ModelForm,TextInput,NumberInput,RadioSelect,DateInput,TimeInput
from django.forms.widgets import HiddenInput

from .models import *
from accounts.models import Customer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from multiselectfield import MultiSelectFormField



class HorizontalRadioSelect(forms.RadioSelect):
    template_name = 'horizontal_select.html'
class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class serviceRequest(ModelForm):
  
    class Meta:
        model = mod20000_service_request 
        exclude = ['date_today','planning_flag']
        widgets={'entered_by':HiddenInput(),'date':DateInput(),'time':TimeInput(),'other':forms.Textarea(attrs={'rows': 2, 'cols': 40})}


class serviceRequestPlans(ModelForm):
 
      
     class Meta:
        model = mod20000_service_planning
        exclude = ['entered_by','date_today','verification','verification_status','verification_failed','qmsstatus','scheduled','completion_date','completedby']
          
        
        widgets={'entered_by':HiddenInput(),'status':forms.HiddenInput,'due':DateInput(),'planning_date':DateInput(),'completion_date':DateInput(), 'description':forms.Textarea(attrs={'rows': 2, 'cols': 40}), 'error':forms.Textarea(attrs={'rows': 2, 'cols': 40}), 'activities':forms.Textarea(attrs={'rows': 2, 'cols': 40}), 'report_number':forms.Textarea(attrs={'rows': 2, 'cols': 40}), 'solution':forms.Textarea(attrs={'rows': 2, 'cols': 40}), 'remark':forms.Textarea(attrs={'rows': 2, 'cols': 40})}

class VerifyServiceRequest(ModelForm):
    class Meta:
        model = mod20000_service_planning 
        #fields = '__all__'
        fields=['due','verification_status','verification_failed','qmsstatus','scheduled','completion_date','completedby','report_number','error','solution','remark','component_affected']
        widgets={'due':HiddenInput(),'completion_date':DateInput(),'scheduled':DateInput(),'verification_failed':forms.Textarea(attrs={'rows': 2, 'cols': 40})}        

