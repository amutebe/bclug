from django.forms import ModelForm,TextInput,NumberInput,RadioSelect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

#######post pack forms#############

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('name', 'birthdate', 'country', 'city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')


##################################


#define dropdown calender for car date
class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'
class ApproveIssue(ModelForm):
    
    
    class Meta:
        model = mod9001_issues 
        #fields = '__all__'
        fields=['status','rejected','approval_date','approved_by']
        widgets={'status': RadioSelect(),'approval_date':DateInput()}

class ApproveIp(ModelForm):
    
    
    class Meta:
        model = mod9001_interestedParties 
        #fields = '__all__'
        fields=['status','rejected','approval_date','approved_by','approval_date']
        widgets={'status': RadioSelect(),'approval_date':DateInput()}

class ApproveRequirement(ModelForm):
    
    
    class Meta:
        model = mod9001_regulatoryReq 
        #fields = '__all__'
        fields=['status','rejected','approval_date','approved_by']
        widgets={'status': RadioSelect(),'approval_date':DateInput()}

class ApproveRisk(ModelForm):
    
    
    class Meta:
        model = mod9001_risks 
        #fields = '__all__'
        fields=['status','rejected','approval_date','approved_by']
        widgets={'status': RadioSelect(),'approval_date':DateInput()}

        
class ApproveOpp(ModelForm):
    
    
    class Meta:
        model = mod9001_risks 
        #fields = '__all__'
        fields=['status','rejected','approval_date','approved_by']
        widgets={'status': RadioSelect(),'approval_date':DateInput()}

class IssuesForm(ModelForm):
    
    class Meta:
        model = mod9001_issues 
        exclude=['approval_date']
        widgets = {
            'analysis_date': DateInput(),'due':DateInput()
        }

class IssuesEdit(ModelForm):
    
    class Meta:
        model = mod9001_issues 
        exclude = ['entered_by','date_today']
        widgets = {
            'analysis_date': DateInput(),'due':DateInput()
        }



class interestedPartiesFORM(ModelForm):
    
    class Meta:
        model = mod9001_interestedParties 
        fields='__all__'
        widgets = {

            'analysis_date': DateInput(),'due':DateInput()
        }



class IPEdit(ModelForm):
    
    class Meta:
        model = mod9001_interestedParties 
        exclude = ['entered_by','date_today']
        widgets = {
            'analysis_date': DateInput(),'due':DateInput()
        }




class regulatoryRequirmentFORM(ModelForm):
    
    class Meta:
        model = mod9001_regulatoryReq 
        fields='__all__'
        widgets = {

            'registered': DateInput(),'due':DateInput()
        }

class regulatoryreqEdit(ModelForm):
    
    class Meta:
        model = mod9001_regulatoryReq 
        exclude = ['entered_by','date_today']
        widgets = {
            'analysis_date': DateInput(),'due':DateInput()
        }

class risk(ModelForm):
    
    class Meta:
        model = mod9001_risks 
        exclude = ['document','opp_number','verification','verification_status','verification_failed','evidence','residuelikelihood','residueseverity','residueriskrating','residueriskrank']
        widgets = {

            'risk_date': DateInput(),'due':DateInput(),'riskrating':TextInput()
        }

class VerifyRisk(ModelForm):
    
    class Meta:
        model = mod9001_risks 
        #fields = '__all__'
        fields=['verification','verification_status','verification_failed','status','document','residuelikelihood','residueseverity','residueriskrating','residueriskrank']

class VerifyOpp(ModelForm):
    
    class Meta:
        model = mod9001_risks 
        #fields = '__all__'
        fields=['verification','verification_status','verification_failed','status','document']



