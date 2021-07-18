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
    request_mode=models.ForeignKey('ServiceRequest_mode', on_delete=models.CASCADE,verbose_name='Request Mode:',null=True,blank=True)
    IT_service=models.ForeignKey('IT_service', on_delete=models.CASCADE,verbose_name='IT service:',null=True,blank=True)
    other=models.TextField("Details",null=True, blank=True)
    priority=models.ForeignKey('priority', on_delete=models.CASCADE,verbose_name='Priority:',null=True,blank=True)
    entered_by = models.ForeignKey(settings.Aup75765-65UTH_USER_MODEL,null=True, blank=True,on_delete=models.CASCADE)
    date_today=models.DateField("Date created:",default=datetime.now)
    planning_flag=models.TextField("Service planning Done?",null=True,blank=True,default='No', help_text='To be uses while filtering serive requests pending planning')
    
    
    
    def __str__(self):
        return self.service_number
        

class service_category(models.Model):

    description=models.CharField("Category:", max_length=50,null=True,blank=True)
    def __str__(self):
        return self.description

class resources(models.Model):

    description=models.CharField("Resource:", max_length=50,null=True,blank=True)
    def __str__(self):
        return self.description

class dependency(models.Model):

    description=models.CharField("Depandency:", max_length=50,null=True,blank=True)
    def __str__(self):
        return self.description

class criteria(models.Model):

    description=models.CharField("Criteria:", max_length=50,null=True,blank=True)
    def __str__(self):
        return self.description

class component(models.Model):

    description=models.CharField("Component:", max_length=50,null=True,blank=True)
    def __str__(self):
        return self.description

class mod20000_service_planning(models.Model):
    service_number=models.OneToOneField('mod20000_service_request', on_delete=models.CASCADE,verbose_name='SR ID:',null=True,blank=True)
    service_category=models.ForeignKey('service_category', on_delete=models.CASCADE,verbose_name='Service Category:',null=True,blank=True)
    rootcause=models.ForeignKey('rootcause', on_delete=models.CASCADE,verbose_name='Root Cause:',null=True,blank=True)
    resource=models.ForeignKey('resources', on_delete=models.CASCADE,verbose_name='Resources:',null=True,blank=True)
    service_dependency=models.ForeignKey('dependency', on_delete=models.CASCADE,verbose_name='Depandency on other services:',null=True,blank=True)
    description=models.TextField("Additional Description:",null=True, blank=True)
    activities=models.TextField("Key Activities:",null=True, blank=True)
    criteria=models.ForeignKey('criteria', on_delete=models.CASCADE,verbose_name='Service Dependency Criteria:',null=True,blank=True)
    assigned = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, verbose_name='AssignedTo:',on_delete=models.CASCADE)
    completion=models.DateField("Completion Date:",null=True,blank=True)
    completedby= models.ForeignKey('accounts.employees',on_delete=models.CASCADE,verbose_name='Completed by:',null=True,blank=True)
    report_number=models.TextField("Report No.:",null=True, blank=True)
    completion_date=models.DateField("Completion Date:",null=True,blank=True) 
    component_affected= models.ForeignKey('component',on_delete=models.CASCADE,verbose_name='Component Affected:',null=True,blank=True)    
    error=models.TextField("Known Error:",null=True, blank=True)    
    Solution=models.TextField("Solution:",null=True, blank=True) 
    remark=models.TextField("Remarks:",null=True, blank=True) 
    
    verification=models.ForeignKey('issues_9001.RISK_OPPverification', on_delete=models.CASCADE,verbose_name='Verification:',null=True,blank=True)
    verification_status=models.CharField(max_length=200, null=True,blank=True)
    verification_failed=models.TextField("Reason for rejecting:",null=True,blank=True, help_text='If rejected, please give a reason')
    qmsstatus=models.ForeignKey(qmsstatus, on_delete=models.CASCADE,null=True,verbose_name='Verification Status:')
    
  
    scheduled=models.DateField("Rescheduled Date:",null=True,blank=True)
    due=models.DateField("When:",null=True,blank=True)      
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True,on_delete=models.CASCADE)
    date_today=models.DateField("Date created:",default=datetime.now)
    status=models.ForeignKey('issues_9001.approval_status', on_delete=models.CASCADE,verbose_name='Status:',null=True,blank=True)
    def __str__(self):
        return self.service_number