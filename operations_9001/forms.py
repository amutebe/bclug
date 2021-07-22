from django.forms import ModelForm,TextInput,NumberInput,RadioSelect

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



class document_manager(ModelForm):
    
    
    class Meta:
        model = mod9001_document_manager 
        fields = '__all__'
        widgets={'author':forms.Textarea(attrs={'rows': 1, 'cols': 40}),'Origin': RadioSelect(),'document_date':DateInput(),'document_id':forms.Textarea(attrs={'rows': 1, 'cols': 40}),'clause':forms.Textarea(attrs={'rows': 1, 'cols': 40}),'doc_name':forms.Textarea(attrs={'rows': 1, 'cols': 40}),'specifyl':forms.Textarea(attrs={'rows': 1, 'cols': 40}),'version':forms.Textarea(attrs={'rows': 1, 'cols': 40}),'Author':forms.Textarea(attrs={'rows': 1, 'cols': 40})}

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
        if end_date is not None and start_date is not None:
            if end_date < start_date:
                raise forms.ValidationError("End date should be greater than start date.")
        else:
            raise forms.ValidationError("End date and Start date cannot be empty")

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
        fields=['verification','verification_status','verification_failed','qmsstatus','scheduled','completion','end']
        widgets={'completion':DateInput(),'scheduled':DateInput()}   

class trainingregister(ModelForm):
  
    class Meta:
        model = mod9001_trainingregister 
        exclude = ['training_desc','trainingplanid','training','location','trainer','entered_by','date_today','verification','verification_status','verification_failed','qmsstatus','scheduled','completion']
        widgets={'status':forms.HiddenInput,'actionplanother':forms.Textarea(attrs={'rows': 2, 'cols': 40}),'reasonother':forms.Textarea(attrs={'rows': 2, 'cols': 40}),'timeline':DateInput(),'train_date':DateInput(),'completion_date':DateInput(),'job':HorizontalRadioSelect(),'skills':HorizontalRadioSelect(),'indicators':HorizontalRadioSelect(),'able':HorizontalRadioSelect()}
    
    def clean(self):
        cleaned_data = super().clean()
        training_date = cleaned_data.get("train_date")
        completion_date = cleaned_data.get("completion_date")

        if completion_date < training_date:
            raise forms.ValidationError("Training date should be less than completion date.")
        
class Verifyetrainingregister(ModelForm):
    class Meta:
        model = mod9001_trainingregister
        #fields = '__all__'
        fields=['verification','verification_status','verification_failed','qmsstatus','scheduled','completion']
        widgets={'completion':DateInput(),'scheduled':DateInput()}        






class trainingplaner(ModelForm):
  
    class Meta:
        model = mod9001_trainingplanner
        exclude=['trainplannerstatus','reason','rescheduled','completion','rejected','approval_date','approved_by','approval_date','verification','verification_status','verification_failed','trainplannerstatus','rescheduled','completion']
        widgets={'trainng_date':DateInput(),'start':DateInput(),'end':DateInput(),'rescheduled':DateInput(),'completion':DateInput()}

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start")
        end_date = cleaned_data.get("end")
        if end_date is not None and start_date is not None:
            if end_date < start_date:
                raise forms.ValidationError("End date should be greater than start date.")
        else:
            raise forms.ValidationError("End date and Start date cannot be empty")

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
        fields=['verification','verification_status','verification_failed','trainplannerstatus','rescheduled','completion','end']
        widgets={'completion':DateInput(),'rescheduled':DateInput()}   


class incident_Register(ModelForm):
  
    class Meta:
        model = mod9001_incidentregister 
        exclude = ['entered_by','date_today','analysis_flag']
        widgets={'date':DateInput(),'time':TimeInput(),'other':forms.Textarea(attrs={'rows': 2, 'cols': 40})}

class customer_Register(ModelForm):
  
    class Meta:
        model = mod9001_customeregistration 
        exclude = ['entered_by','date_today']
        widgets={'date_posted':DateInput()}

class incident_RegisterStaff(ModelForm):
     #cost = MultiSelectFormField(choices=mod9001_incidentregisterStaff.costs)
      
     class Meta:
        model = mod9001_incidentregisterStaff
        #exclude = ['entered_by','date_today','status']
        exclude = ['cost','currency','costdescription','lesson','entered_by','date_today','verification','verification_status','verification_failed','qmsstatus','scheduled','completion','report_number','error','solution','component_affected','remark']
          
        
        widgets={'status':forms.HiddenInput,'due':DateInput(),'date':DateInput(),'completion':DateInput(),'date_posted':DateInput(), 'costdescription':forms.Textarea(attrs={'rows': 2, 'cols': 40}), 'lesson':forms.Textarea(attrs={'rows': 2, 'cols': 40}), 'description':forms.Textarea(attrs={'rows': 2, 'cols': 40})}
class Verifyincidentregister(ModelForm):
    class Meta:
        model = mod9001_incidentregisterStaff 
        #fields = '__all__'
        fields=['cost','currency','costdescription','verification','verification_status','verification_failed','qmsstatus','scheduled','completion','report_number','error','solution','component_affected','remark']
        widgets={'completion':DateInput(),'scheduled':DateInput(),'verification_failed':forms.Textarea(attrs={'rows': 2, 'cols': 40}),'report_no':forms.Textarea(attrs={'rows': 2, 'cols': 40}),'error':forms.Textarea(attrs={'rows': 2, 'cols': 40}),'remark':forms.Textarea(attrs={'rows': 2, 'cols': 40}),'solution':forms.Textarea(attrs={'rows': 2, 'cols': 40})}        



class providerassessments(ModelForm):

     #cost = MultiSelectFormField(choices=mod9001_incidentregisterStaff.costs)
      
    class Meta:
        model = mod9001_providerassessment 
        exclude = ['cost','currency','costdescription','lesson','entered_by','date_today','verification','verification_status','verification_failed','qmsstatus','scheduled','completion']

            
 
        

        #fields = ['emp_perfrev_no','planner_number','date','Provider','organisation','assesment_date','start','end','appraise']
       
        
        widgets={'status':forms.HiddenInput,'nonconfdetails':forms.Textarea(attrs={'rows': 2, 'cols': 40}),'due':DateInput(),'comment':forms.Textarea(attrs={'rows': 2, 'cols': 40}),'purpose':forms.Textarea(attrs={'rows': 2, 'cols': 40}),'date':DateInput(),'assesment_date':DateInput(),'start':DateInput(), 'end':DateInput(),'jobknowledge':HorizontalRadioSelect(),'adaptability':HorizontalRadioSelect(),'problemsolve':HorizontalRadioSelect(),'initiativeness':HorizontalRadioSelect(),'planning':HorizontalRadioSelect(),'work':HorizontalRadioSelect(),'Communication':HorizontalRadioSelect(),'skills':HorizontalRadioSelect(),'supervision':HorizontalRadioSelect(),'availability':HorizontalRadioSelect(),'professionalism':HorizontalRadioSelect()}
    def clean(self):
        cleaned_data = super().clean()
        last_date = cleaned_data.get("assesment_date")
        start_date = cleaned_data.get("start")
        end_date = cleaned_data.get("end")
        due_date = cleaned_data.get("due")
        
        
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")
        elif last_date > start_date:
            raise forms.ValidationError("Last assessment date should not be greater than start date.")
        elif due_date < end_date:
            raise forms.ValidationError("When date should not be less than end date.")

        



class Verifyeproviderassessments(ModelForm):
    class Meta:
        model = mod9001_providerassessment 
        #fields = '__all__'
        fields=['cost','currency','costdescription','verification','verification_status','verification_failed','qmsstatus','scheduled','completion']
        widgets={'completion':DateInput(),'scheduled':DateInput()}        


class corrective_action(ModelForm):
    
    class Meta:
        model = mod9001_correctiveaction 
        exclude = ['entered_by','date_today','car_flag']
        widgets = {

            'date': DateInput(),'reference':forms.Textarea(attrs={'rows': 2, 'cols': 40}),'addesc':forms.Textarea(attrs={'rows': 2, 'cols': 40})
        }

class mod9001planning(ModelForm):
    
    class Meta:
        model = mod9001_planning 
        exclude = ['completion','qmsstatus','scheduled','entered_by','date_today','verification','verification_status','verification_failed','rejected','approval_date','approved_by']
        widgets = {

           'comment':forms.Textarea(attrs={'rows': 2, 'cols': 40}),'status':forms.HiddenInput, 'due': DateInput(),'rootcause_desc':forms.Textarea(attrs={'rows': 2, 'cols': 40}),'details':forms.Textarea(attrs={'rows': 2, 'cols': 40})
        }

   
class VerifyPlanning(ModelForm):
    
    class Meta:
        model = mod9001_planning 
        #fields = '__all__'
        fields=['verification','verification_status','verification_failed','qmsstatus','scheduled','completion']
        widgets={'completion':DateInput(),'scheduled':DateInput()} 


class ApprovePlanning(ModelForm):
    
    
    class Meta:
        model = mod9001_planning 
        #fields = '__all__'
        fields = ['status','rejected','approval_date','approved_by']
        widgets={'status': RadioSelect(),'approval_date':DateInput()}


class change_request(ModelForm):
    
    class Meta:
        model = mod9001_changeRegister 
        fields = ['status','req_no','date','raisedby','trigger','reference','process','changetype','changedesc']
        #exclude = ['status','proposedby','assignedto','due','completion','qmsstatus','scheduled','entered_by','date_today','verification','verification_status','verification_failed','rejected','approval_date','approved_by']
        widgets = {

            'status':forms.HiddenInput,'date': DateInput(),'due': DateInput(),'reference':forms.Textarea(attrs={'rows': 2, 'cols': 40}),'changedesc':forms.Textarea(attrs={'rows': 2, 'cols': 40})
        }

class ApproveChangeRequest(ModelForm):
    
    
    class Meta:
        model = mod9001_changeRegister 
        #fields = '__all__'
        fields = ['status','rejected','approval_date','approved_by','evaluation','evaldesc','cost','currency','costdescription','add_desc']
        widgets={'status': RadioSelect(),'approval_date':DateInput(),'evaldesc':forms.Textarea(attrs={'rows': 2, 'cols': 40}),'add_desc':forms.Textarea(attrs={'rows': 2, 'cols': 40})
        }


class Verifychangerequest(ModelForm):
    
    class Meta:
        model = mod9001_changeRegister 
        #fields = '__all__'
        fields=['verification','verification_status','verification_failed','qmsstatus','scheduled','completion']
        widgets={'completion':DateInput(),'scheduled':DateInput()} 


class customer_complaint(ModelForm):
     #cost = MultiSelectFormField(choices=mod9001_incidentregisterStaff.costs)
      
     class Meta:
        model = mod9001_customerComplaint
        #exclude = ['entered_by','date_today','status']
        exclude = ['analysis_flag','entered_by','date_today','verification','verification_status','verification_failed','qmsstatus','scheduled','completion','re_occurance','classification','correction','add_desc','assignedto','due']
 
        widgets={'complaint':TextInput(),'time':TimeInput(),'status':forms.HiddenInput,'due':DateInput(),'date':DateInput(),'completion':DateInput(),'date_posted':DateInput(), 'complaint_desc':forms.Textarea(attrs={'rows': 2, 'cols': 40})}

class customer_complaintPlanning(ModelForm):
     #cost = MultiSelectFormField(choices=mod9001_incidentregisterStaff.costs)
      
     class Meta:
        model = mod9001_customerComplaint
        #exclude = ['entered_by','date_today','status']
        fields = ['re_occurance','classification','correction','add_desc','assignedto','due','analysis_flag']
 
        widgets={'time':TimeInput(),'status':forms.HiddenInput,'analysis_flag':forms.HiddenInput,'due':DateInput(),'date':DateInput(),'completion':DateInput(),'date_posted':DateInput(), 'complaint_desc':forms.Textarea(attrs={'rows': 2, 'cols': 40}), 'add_desc':forms.Textarea(attrs={'rows': 2, 'cols': 40})}

class Verifycustomer_complaint(ModelForm):
    class Meta:
        model = mod9001_customerComplaint 
        #fields = '__all__'
        fields=['verification','verification_status','verification_failed','qmsstatus','scheduled','completion']
        widgets={'completion':DateInput(),'scheduled':DateInput()}        




class customersatisfaction_email(ModelForm):# to auntenticate customer byemail input before displaying the survet form
    class Meta:
        model = Customer
        #fields = '__all__'
        fields=['email']
        #widgets={'email':emailInput()}        




class customer_satisfaction_survey(ModelForm): #for customers outside company without login accounts

     #cost = MultiSelectFormField(choices=mod9001_incidentregisterStaff.costs)
      
    class Meta:
        model = mod9001_customerSatisfaction 
        exclude = ['start','end','entered_by','date_today','verification','verification_status','verification_failed','qmsstatus','scheduled','completion','improvplan','details','due','assignedto']
        #widgets={'improvplan':forms.HiddenInput,'details':forms.HiddenInput,'assignedto':forms.HiddenInput,'due':forms.HiddenInput,'end':DateInput(),'start':DateInput(),'status':forms.HiddenInput,'comment':forms.Textarea(attrs={'rows': 2, 'cols': 40}),'due':DateInput(),'details':forms.Textarea(attrs={'rows': 2, 'cols': 40}),'date':DateInput(),'responsetime':HorizontalRadioSelect(),'resolution':HorizontalRadioSelect(),'delivery':HorizontalRadioSelect(),'communication':HorizontalRadioSelect(),'compliant':HorizontalRadioSelect(),'quality':HorizontalRadioSelect(),'infosecurity':HorizontalRadioSelect(),'customerservice':HorizontalRadioSelect()}
        widgets={'end':DateInput(),'start':DateInput(),'status':forms.HiddenInput,'comment':forms.Textarea(attrs={'rows': 2, 'cols': 40}),'due':DateInput(),'details':forms.Textarea(attrs={'rows': 2, 'cols': 40}),'date':DateInput(),'responsetime':HorizontalRadioSelect(),'resolution':HorizontalRadioSelect(),'delivery':HorizontalRadioSelect(),'communication':HorizontalRadioSelect(),'compliant':HorizontalRadioSelect(),'quality':HorizontalRadioSelect(),'infosecurity':HorizontalRadioSelect(),'customerservice':HorizontalRadioSelect()}
    
    
    #def clean(self):
    #    cleaned_data = super().clean()
    #    start_date = cleaned_data.get("start")
    #    end_date = cleaned_data.get("end")
    #    if end_date is not None and start_date is not None:
    #        if end_date < start_date:
    #            raise forms.ValidationError("End date should be greater than start date.")
    #    else:
    #        raise forms.ValidationError("End date and Start date cannot be empty")
        
 
        


class customer_satisfaction(ModelForm): # for company staff that require login accounts

     #cost = MultiSelectFormField(choices=mod9001_incidentregisterStaff.costs)
      
    class Meta:
        model = mod9001_customerSatisfaction 
        exclude = ['entered_by','date_today','verification','verification_status','verification_failed','qmsstatus','scheduled','completion']

            
 
        

        #fields = ['emp_perfrev_no','planner_number','date','Provider','organisation','assesment_date','start','end','appraise']
       
        
        widgets={'end':DateInput(),'start':DateInput(),'status':forms.HiddenInput,'comment':forms.Textarea(attrs={'rows': 2, 'cols': 40}),'due':DateInput(),'details':forms.Textarea(attrs={'rows': 2, 'cols': 40}),'date':DateInput(),'responsetime':HorizontalRadioSelect(),'resolution':HorizontalRadioSelect(),'delivery':HorizontalRadioSelect(),'communication':HorizontalRadioSelect(),'compliant':HorizontalRadioSelect(),'quality':HorizontalRadioSelect(),'infosecurity':HorizontalRadioSelect(),'customerservice':HorizontalRadioSelect()}
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start")
        end_date = cleaned_data.get("end")
        if end_date is not None and start_date is not None:
            if end_date < start_date:
                raise forms.ValidationError("End date should be greater than start date.")
        else:
            raise forms.ValidationError("End date and Start date cannot be empty")

class Verifyecustomersatisfaction(ModelForm):
    class Meta:
        model = mod9001_customerSatisfaction 
        #fields = '__all__'
        fields=['verification','verification_status','verification_failed','qmsstatus','scheduled','completion']
        widgets={'completion':DateInput(),'scheduled':DateInput()}        

