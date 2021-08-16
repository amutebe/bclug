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
        widgets={'record_group':HiddenInput(),'requestor':forms.Textarea(attrs={'rows': 2, 'cols': 40}),'entered_by':HiddenInput(),'date':DateInput(),'time':TimeInput(),'other':forms.Textarea(attrs={'rows': 2, 'cols': 40})}


class serviceRequestPlans(ModelForm):
 
      
     class Meta:
        model = mod20000_service_planning
        exclude = ['document','entered_by','date_today','verification','verification_status','verification_failed','qmsstatus','scheduled','completion_date','completedby', 'component_affected','error','solution','report_number']
          
        
        widgets={'record_group':HiddenInput(),'entered_by':HiddenInput(),'status':forms.HiddenInput,'due':DateInput(),'planning_date':DateInput(),'completion_date':DateInput(), 'description':forms.Textarea(attrs={'rows': 2, 'cols': 40}), 'error':forms.Textarea(attrs={'rows': 2, 'cols': 40}), 'activities':forms.Textarea(attrs={'rows': 2, 'cols': 40}), 'report_number':forms.Textarea(attrs={'rows': 2, 'cols': 40}), 'solution':forms.Textarea(attrs={'rows': 2, 'cols': 40}), 'remark':forms.Textarea(attrs={'rows': 2, 'cols': 40})}

     def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("planning_date")
        end_date = cleaned_data.get("due")

            
        if end_date is not None and start_date is not None:
            if end_date < start_date:
                raise forms.ValidationError("When date should be greater than Planning date.")
        else:
            raise forms.ValidationError("When date and Planning date cannot be empty")



class VerifyServiceRequest(ModelForm):
    class Meta:
        model = mod20000_service_planning 
        #fields = '__all__'
        fields=['planning_date','due','qmsstatus','scheduled','completion_date','completedby','verification_failed','report_number','error','solution','remark','component_affected','document']
        widgets={'report_number':forms.Textarea(attrs={'rows': 1, 'cols': 60}),'error':forms.Textarea(attrs={'rows': 3, 'cols': 60}),'solution':forms.Textarea(attrs={'rows': 3, 'cols': 60}),'remark':forms.Textarea(attrs={'rows': 3, 'cols': 60}),'planning_date':HiddenInput(),'due':HiddenInput(),'completion_date':DateInput(),'scheduled':DateInput(),'verification_failed':forms.Textarea(attrs={'rows': 3, 'cols': 60}),'verification_status':forms.Textarea(attrs={'rows': 3, 'cols': 60})}        

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("planning_date")
        end_date = cleaned_data.get("completion_date")
        reschedule_date = cleaned_data.get("scheduled")
            
     #   print("PRINT",end_date,start_date)
        if end_date is not None and start_date is not None:
            if end_date < start_date or end_date>date.today() :
                raise forms.ValidationError("Completion date shouldn't be less than Planning date or be in Future")

        
        elif reschedule_date is not None and start_date is not None:
           if reschedule_date < start_date or reschedule_date < date.today():
                raise forms.ValidationError("Reschedule date shouldn't be less than Planning date or today's date")

        else:
            raise forms.ValidationError("Completion date or Reschedule date cannot be empty")


        
