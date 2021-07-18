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
        exclude = ['cost','currency','costdescription','lesson','entered_by','date_today','verification','verification_status','verification_failed','qmsstatus','scheduled','completion']
          
        
        widgets={'status':forms.HiddenInput,'due':DateInput(),'date':DateInput(),'completion':DateInput(),'date_posted':DateInput(), 'costdescription':forms.Textarea(attrs={'rows': 2, 'cols': 40}), 'lesson':forms.Textarea(attrs={'rows': 2, 'cols': 40}), 'description':forms.Textarea(attrs={'rows': 2, 'cols': 40})}
class Verifyincidentregister(ModelForm):
    class Meta:
        model = mod9001_incidentregisterStaff 
        #fields = '__all__'
        fields=['cost','currency','costdescription','verification','verification_status','verification_failed','qmsstatus','scheduled','completion']
        widgets={'completion':DateInput(),'scheduled':DateInput(),'verification_failed':forms.Textarea(attrs={'rows': 2, 'cols': 40})}        

