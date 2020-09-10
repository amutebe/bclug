from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

#define dropdown calender for car date
class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'



class CARForm(ModelForm):
    
    class Meta:
        model = car 
        #fields = '__all__'
        fields=['car_number','car_dateoccur','car_time','car_dept','car_userid','nonconf']
        widgets = {
            'car_dateoccur': DateInput(), 'car_time':TimeInput()
        }

class CARs(ModelForm):
    
    class Meta:
        model = car 
        #fields = '__all__'
        #fields=['car_number','car_dateoccur','car_time','car_dept','car_userid','nonconf']
        fields=['car_number', 'car_dateoccur', 'car_dept', 'car_userid', 'nonconf','description','action','CAother','rootcause','Rootother','correctiveaction','correctiveactionOther',
'proposedby','proposedDate','deadline', 'priority','implementedby','entered_by','status']
        widgets = {
            'car_dateoccur': DateInput(), 'car_time':TimeInput(),'proposedDate': DateInput(),
            'deadline': DateInput(),'car_date': DateInput()
        }

       


class ApproveCar(ModelForm):
    
    class Meta:
        model = car 
        #fields = '__all__'
        fields=['status','rejected']

class VerifyCar(ModelForm):
    
    class Meta:
        model = car 
        #fields = '__all__'
        fields=['verification','verification_status','verification_failed','status']


class CARFormSave(ModelForm):
    
    class Meta:
        model = car
        fields = '__all__' 
        #fields = ['car_number','car_dept_id','car_userid_id','nonconf_id','description','action','rootcause_id','correctiveaction_id','proposedby_id','implementedby_id','deadline']
        

class CARapproveForm(ModelForm):
    
    class Meta:
        model = car 
        exclude=['nonconf','car_issue']

class CAReditForm(ModelForm):
    
    class Meta:
        model = car 
        exclude=['car_date','status','rejected','verification','verification_status','verification_failed']
        widgets = {
            'car_dateoccur': DateInput(), 'car_time':TimeInput(),'proposedDate': DateInput(),
            'deadline': DateInput(),'car_date': DateInput()
        }

class OrderForm(ModelForm):
    
    class Meta:
        model = Order 
        fields = '__all__'


class CreateUser(UserCreationForm):
    
    class meta:
        model=User
        fields=['username','password1','password2','email']


