from django.forms import ModelForm,TextInput,NumberInput,RadioSelect

from .models import *
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



class document_manager(ModelForm):
    
    
    class Meta:
        model = mod9001_document_manager 
        fields = '__all__'
        widgets={'Origin': RadioSelect(),'document_date':DateInput()}

class calibration(ModelForm):
    
    
    class Meta:
        model = mod9001_calibration 
        fields = '__all__'
        widgets={'calibration_date':DateInput()}

class mentainance(ModelForm):
    
    
    class Meta:
        model = maintenance 
        fields = '__all__'
        widgets={'date_today':DateInput(),'date':DateInput()}

class qmsplanner(ModelForm):
  
    class Meta:
        model = mod9001_qmsplanner 
        fields = ['planner_number','plan_date','planner','start','end','description','details','status']
        widgets={'plan_date':DateInput(),'start':DateInput(),'end':DateInput(),'due':DateInput()}

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start")
        end_date = cleaned_data.get("end")
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")

class ApproveQMS(ModelForm):

    
    
    class Meta:
        model = mod9001_qmsplanner 
        #fields = '__all__'
        fields=['status','rejected','approval_date','approved_by','approval_date']
        widgets={'status': RadioSelect(),'approval_date':DateInput()}      

class VerifyQMS(ModelForm):
    
    class Meta:
        model = mod9001_qmsplanner 
        #fields = '__all__'
        fields=['verification','verification_status','verification_failed','qmsstatus','scheduled','completion']
        widgets={'completion':DateInput(),'scheduled':DateInput()}   

class trainingregister(ModelForm):
  
    class Meta:
        model = mod9001_trainingregister 
        exclude = ['training_desc','trainingplanid','training','location','trainer','entered_by','date_today']
        widgets={'train_date':DateInput(),'completion_date':DateInput(),'job':HorizontalRadioSelect(),'skills':HorizontalRadioSelect(),'indicators':HorizontalRadioSelect(),'able':HorizontalRadioSelect()}

class trainingplaner(ModelForm):
  
    class Meta:
        model = mod9001_trainingplanner
        exclude=['trainplannerstatus','reason','rescheduled','completion','rejected','approval_date','approved_by','approval_date','verification','verification_status','verification_failed','trainplannerstatus','rescheduled','completion']
        widgets={'trainng_date':DateInput(),'start':DateInput(),'end':DateInput(),'rescheduled':DateInput(),'completion':DateInput()}

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start")
        end_date = cleaned_data.get("end")
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")

class ApproveTrainingPlanner(ModelForm):
   
    
    class Meta:
        model = mod9001_trainingplanner 
        #fields = '__all__'
        fields=['status','rejected','approval_date','approved_by','approval_date']
        widgets={'status': RadioSelect(),'approval_date':DateInput()}  


class VerifyTraining(ModelForm):
    
    class Meta:
        model = mod9001_trainingplanner 
        #fields = '__all__'
        fields=['verification','verification_status','verification_failed','trainplannerstatus','rescheduled','completion']
        widgets={'completion':DateInput(),'rescheduled':DateInput()}   


class incident_Register(ModelForm):
  
    class Meta:
        model = mod9001_incidentregister 
        exclude = ['entered_by','date_today']
        widgets={'date':DateInput(),'time':TimeInput()}

class customer_Register(ModelForm):
  
    class Meta:
        model = mod9001_customeregistration 
        exclude = ['entered_by','date_today']
        widgets={'date_posted':DateInput()}

class incident_RegisterStaff(ModelForm):
     #cost = MultiSelectFormField(choices=mod9001_incidentregisterStaff.costs)
      
     class Meta:
        model = mod9001_incidentregisterStaff 
        exclude = ['entered_by','date_today','status']
        
        widgets={'date':DateInput(),'completion':DateInput(),'date_posted':DateInput(), 'costdescription':forms.Textarea(attrs={'rows': 2, 'cols': 40}), 'status':forms.Textarea(attrs={'rows': 2, 'cols': 40}), 'lesson':forms.Textarea(attrs={'rows': 2, 'cols': 40}), 'description':forms.Textarea(attrs={'rows': 2, 'cols': 40})}

class providerassessments(ModelForm):
     #cost = MultiSelectFormField(choices=mod9001_incidentregisterStaff.costs)
      
     class Meta:
        model = mod9001_providerassessment 
        exclude = ['entered_by','date_today']
        

        #fields = ['emp_perfrev_no','planner_number','date','Provider','organisation','assesment_date','start','end','appraise']
       
        
        widgets={'comment':TextInput(),'purpose':TextInput(),'date':DateInput(),'assesment_date':DateInput(),'start':DateInput(), 'end':DateInput(),'jobknowledge':HorizontalRadioSelect(),'adaptability':HorizontalRadioSelect(),'problemsolve':HorizontalRadioSelect(),'initiativeness':HorizontalRadioSelect(),'planning':HorizontalRadioSelect(),'work':HorizontalRadioSelect(),'Communication':HorizontalRadioSelect(),'skills':HorizontalRadioSelect(),'supervision':HorizontalRadioSelect(),'availability':HorizontalRadioSelect(),'professionalism':HorizontalRadioSelect()}
        def clean(self):
            cleaned_data = super().clean()
            start_date = cleaned_data.get("start")
            end_date = cleaned_data.get("end")
            if end_date < start_date:
                raise forms.ValidationError("End date should be greater than start date.")







   
