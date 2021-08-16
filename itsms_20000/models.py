from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from random import randint,randrange
from django import forms
from django.conf import settings
from multiselectfield import MultiSelectField
from accounts.utils import *

# Create your models here.
class ServiceRequest_type(models.Model):

    description=models.CharField("Request Type:", max_length=50,null=True,blank=True)
    def __str__(self):
        return self.description

class ServiceRequest_mode(models.Model):

    description=models.CharField("Request Mode:", max_length=50,null=True,blank=True)
    def __str__(self):
        return self.description


class IT_service(models.Model):

    description=models.CharField("IT Service:", max_length=50,null=True,blank=True)
    def __str__(self):
        return self.description

class priority(models.Model):

    description=models.CharField("Priority:", max_length=50,null=True,blank=True)
    def __str__(self):
        return self.description


class mod20000_service_request(models.Model):
    service_number=models.CharField("SR ID.:",max_length=200,primary_key=True)
    date=models.DateField("Request Date:",null=False)
    time=models.TimeField("Time (24Hr):",null=True)
    request_type=models.ForeignKey('ServiceRequest_type', on_delete=models.CASCADE,verbose_name='Request Type:',null=True,blank=True)
    requestor=models.TextField("Requestor",null=True,blank=True)   
    request_mode=models.ForeignKey('ServiceRequest_mode', on_delete=models.CASCADE,verbose_name='Request Mode:',null=True,blank=True)
    IT_service=models.ForeignKey('IT_service', on_delete=models.CASCADE,verbose_name='IT service:',null=True,blank=True)
    other=models.TextField("Details",null=True, blank=True)
    priority=models.ForeignKey('priority', on_delete=models.CASCADE,verbose_name='Priority:',null=True,blank=True)
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True,on_delete=models.CASCADE,related_name='SrequestBy')
    date_today=models.DateField("Date created:",default=datetime.now)
    planning_flag=models.TextField("Service planning Done?",null=True,blank=True,default='No', help_text='To be uses while filtering serive requests pending planning')
    record_group=models.CharField("Data Group",max_length=20,null=True,blank=True)    
    
    
    def __str__(self):
        return self.service_number
        

class service_category(models.Model):

    description=models.CharField("Category:", max_length=50,null=True,blank=True)
    def __str__(self):
        return self.description

#class resources(models.Model):

#    description=models.CharField("Resource:", max_length=50,null=True,blank=True)
#    def __str__(self):
#       return self.description

#class dependency(models.Model):

#    description=models.CharField("Depandency:", max_length=50,null=True,blank=True)
#    def __str__(self):
#        return self.description

#class criteria(models.Model):

#    description=models.CharField("Criteria:", max_length=50,null=True,blank=True)
#    def __str__(self):
 #       return self.description

class component(models.Model):

    description=models.CharField("Component:", max_length=50,null=True,blank=True)
    def __str__(self):
        return self.description

class scope(models.Model):

    description=models.CharField("Scope:", max_length=50,null=True,blank=True)
    def __str__(self):
        return self.description

class mod20000_service_planning(models.Model):
    service_number=models.OneToOneField('mod20000_service_request', on_delete=models.CASCADE,verbose_name='SR ID:',null=True,blank=True)
    planning_date=models.DateField("Date:",null=False)    
    service_scope=models.ForeignKey('scope', on_delete=models.SET_NULL,verbose_name='Service scope:',null=True,blank=True)   
    service_category=models.ForeignKey('service_category', on_delete=models.SET_NULL,verbose_name='Service Category:',null=True,blank=True)
    #resource=models.ForeignKey('resources', on_delete=models.SET_NULL,verbose_name='Resources:',null=True,blank=True)
    resources=(('1','Transport'),('2','Tools'),('3','License'),('4','Software'),('5','Internet'),('6','Desktop/Laptop'),('7','Voice/Telephone'),('8','Docuentation'),('9','Other'))
    resource = MultiSelectField('Resources',choices=resources,null=True,blank=True)    
    #service_dependency=models.ForeignKey('dependency', on_delete=models.SET_NULL,verbose_name='Depandency on other services:',null=True,blank=True)
    dependencies=(('1','Hardware/ Software Supplies'),('2','IT Support Services'),('3','Installation and Configuration Services'),('4','Procurement Services'),('5','Repair and Maintenance Services'),('6','Storage Services'),('7','CCTV Security Services'),('8','Access and Security (AD, Firewall)'),('9','Backup and Maintenance'),('10','Internet Services'),('11','Communication Services (Email, Telephone and PABX)'),('12','Backup and Maintenance'),('13','Personal Computing (PCs, Printers, Accessories, Software, Apps. etc.)'),('14','Other'))
    dependency = MultiSelectField('Depandency on other services:',choices=dependencies,null=True,blank=True)   
    
    description=models.TextField("Additional Description:",null=True, blank=True)
    activities=models.TextField("Key Activities:",null=True, blank=True)
    #criteria=models.ForeignKey('criteria', on_delete=models.SET_NULL,verbose_name='Service Dependency Criteria:',null=True,blank=True)
    criterias=(('1','Job card'),('2','Completion report/Certificate'),('3','Customer sign off acknowledgement'))
    criteria = MultiSelectField('Criteria',choices=criterias,null=True,blank=True)     
    
    assigned = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, verbose_name='AssignedTo:',on_delete=models.SET_NULL)
    completedby= models.ForeignKey('accounts.employees',on_delete=models.SET_NULL,verbose_name='Completed by:',null=True,blank=True)
    report_number=models.TextField("Report No.:",null=True, blank=True)
    completion_date=models.DateField("Completion Date:",null=True,blank=True) 
    component_affected= models.ForeignKey('component',on_delete=models.SET_NULL,verbose_name='Component Affected:',null=True,blank=True)    
    error=models.TextField("Known Error:",null=True, blank=True)    
    solution=models.TextField("Solution:",null=True, blank=True) 
    remark=models.TextField("Remarks:",null=True, blank=True) 
    
    #verification=models.ForeignKey('issues_9001.RISK_OPPverification', on_delete=models.SET_NULL,verbose_name='Verification:',null=True,blank=True)
    verification_status=models.TextField(max_length=200, null=True,blank=True)
    verification_failed=models.TextField("Reason for rejecting:",null=True,blank=True)
    qmsstatus=models.ForeignKey('operations_9001.qmsstatus', on_delete=models.SET_NULL,null=True,verbose_name='Verification Status:')
    record_group=models.CharField("Data Group",max_length=20,null=True,blank=True)    
  
    scheduled=models.DateField("Rescheduled Date:",null=True,blank=True)
    due=models.DateField("When:",null=True,blank=True)      
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True,on_delete=models.SET_NULL,related_name='planning')
    date_today=models.DateField("Date created:",default=datetime.now)
    status=models.ForeignKey('issues_9001.approval_status', on_delete=models.SET_NULL,verbose_name='Status:',null=True,blank=True)
    document = models.FileField("Upload Support Document:",upload_to='documents/',null=True,blank=True,validators=[validate_file_size])
    uploaded_at = models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
       return str(self.service_number)