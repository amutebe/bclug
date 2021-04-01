from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from random import randint
from django import forms
from django.conf import settings

# Create your models here.
##########################POST BACK MODEL EXAMPLE####################################
class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=100)
    birthdate = models.DateField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
###############################END POST BACK#############################################

def car_no():
    now = datetime.now()
    t=(now.strftime('%H'))+(now.strftime('%M'))+(now.strftime('%S'))
    return str((date.today()).strftime("%d%m%Y"))+str(randint(0, 999))

class approval_status(models.Model):

    description=models.CharField("Approval status", max_length=50,null=True,blank=True)
    
    def __str__(self):
        return self.description

class RISK_OPPverification(models.Model):

    description=models.CharField("CAR verification", max_length=50,null=True,blank=True)
    def __str__(self):
        return self.description

class process_StrengthWeakness(models.Model):

    description=models.CharField("Process Strength/Weakness", max_length=50,null=True,blank=True)
    def __str__(self):
        return self.description

class process_OpportunitiesThreats(models.Model):

    description=models.CharField("Process Opportunities/Threats", max_length=50,null=True,blank=True)
    def __str__(self):
        return self.description

class mod9001_issues(models.Model):
    issue_number=models.CharField("Issue no.:",max_length=200,default="TEGA-CT-Q-"+car_no(),primary_key=True)
    analysis_date=models.DateField("Date of Analysis:")
    analyst= models.ForeignKey('accounts.employees',on_delete=models.CASCADE,verbose_name='Lead Analyst:',related_name='analyst')
    CONTEXT=(('1','Internal Issues'),('2','External Issues'),('3','Process Issues'))
    context=models.CharField(max_length=200,null=False, choices=CONTEXT)
    INTERNAL_ISSUES=(('1','Organisational Culture'),('2','Organisational Knowledge'),('3','Company Values'),('4','ICT Infrastructure'),('5','Available Resources'),('6','Organisational Structure'),('7','Strength'),('8','Weaknesses'),('9','Other'))
    internal_issues=models.CharField(max_length=200,null=True,blank=True, choices=INTERNAL_ISSUES)
    EXTERNAL_ISSUES=(('1','Legal and Regulatory requirements'),('2','Economic enviroment'),('3','Cultural enviroment'),('4','Political enviroment'),('5','Competitive enviroment'),('6','Social enviroment'),('7','Threats'),('8','Opportunities'),('9','Other'))
    external_issues=models.CharField(max_length=200,null=True,blank=True, choices=EXTERNAL_ISSUES)
    process_desc=(('1','Transport'),('2','Sales'),('3','Administration'),('4','Marketing'),('5','Customer Relations'),('6','Service/Help Desk Support'),('7','Inventory'),('8','Project Management'),('9','Procurement'),('10','Other'),('11','Management'),('12','Training'),('13','Recruitment'),('14','Systems Administration'),('15','Disciplinary Process'))
    process_desc=models.CharField("Process Description",max_length=200,null=True,blank=True, choices=process_desc)
    #process_desc= models.ForeignKey('operations_9001.process',on_delete=models.CASCADE,verbose_name='Process:',related_name='Processes')

    PROCESS_ISSUES=(('1','Strength'),('2','Weaknesses'),('3','Opportunities'),('4','Threats'))
    process_issues=models.CharField(max_length=200,null=True,blank=True, choices=PROCESS_ISSUES)
    process_StrengthWeakness=models.ForeignKey(process_StrengthWeakness, on_delete=models.CASCADE,verbose_name='process Strength/Weakness:',related_name='process_StrengthWeakness',null=True,blank=True)
    process_OpportunitiesThreats=models.ForeignKey(process_OpportunitiesThreats, on_delete=models.CASCADE,verbose_name='Process Opportunities/Threats:',related_name='process_OpportunitiesThreats',null=True,blank=True)
    otherIssue=models.TextField("Other Issue:",null=True,blank=True, help_text='Please specify other')

    
    description=models.TextField("Description:",null=True,blank=True, help_text='Please give comments if any')

    mitigation=models.TextField("Mitigation Action:",null=True,blank=True, help_text='Please give description if any')
    responsibility= models.ForeignKey('accounts.employees',on_delete=models.CASCADE,verbose_name='Responsibility:',related_name='responsibility',null=True,blank=True)
    due=models.DateField("When:",null=True,blank=True)
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, related_name='issue_entered_by',on_delete=models.SET_NULL)
    date_today=models.DateField("Date created:",default=datetime.now)
    status=models.ForeignKey(approval_status, on_delete=models.SET_NULL,null=True,verbose_name='Status:')
    rejected=models.TextField("Reason for rejecting:",null=True,blank=True, help_text='If rejected, please give a reason')
    approval_date=models.DateField("Date Approved:",null=True,blank=True)
    approved_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, related_name='Approv_by',on_delete=models.SET_NULL)

    def __str__(self):
        return self.issue_number



class mod9001_interestedParties(models.Model):
    ip_number=models.CharField("IP No.:",max_length=200,default="TEGA-IP-Q-"+car_no(),primary_key=True)
    analysis_date=models.DateField("Date of Analysis:")
    analyst= models.ForeignKey('accounts.employees',on_delete=models.CASCADE,verbose_name='Lead Analyst:')
    IPTYPE=(('1','Internal IP'),('2','External IP'))
    context=models.CharField(max_length=200,null=False, choices=IPTYPE)
    INTERNAL_ISSUES=(('1','Employee/Staff'),('2','Executive Management'),('3','Top Management'))
    internal_issues=models.CharField(max_length=200,null=True,blank=True, choices=INTERNAL_ISSUES)
    EXTERNAL_ISSUES=(('1','Customers'),('2','Regulators'),('3','Hardware/Equipment Suppliers'),('4','Traning providers'),('5','Security providers'),('6','Internet providers'),('7','Insurance providers'),('8','Auditors'),('9','Certification bodies'),('10','Inspectors'),('11','Business partners'),('12','Competitors'),('13','Neighbourhood'),('14','Local authorities'),('15','Family'))
    external_issues=models.CharField(max_length=200,null=True,blank=True, choices=EXTERNAL_ISSUES)
    Quality_needs=(('1','Communication'),('2','Reporting'),('3','Tax complaince'),('4','CSR'),('5','Time payment for services/products'),('6','Timely delivery'),('7','Safe work enviroment'),('8','Operation support'),('9','Work equipment'),('10','Training'),('11','Clear vision'),('12','Quality support'),('13','Performance feedback'),('14','Contractual complaince'),('15','legal complaince'),('16','Business growth'),('17','Performance'))
    quality_needs=models.CharField("Requirement",max_length=200,null=False, choices=Quality_needs)
    description=models.TextField("Description:",null=True,blank=True, help_text='Please give description if any')
    INTERESTEDPARTIES=(('1','Control'),('2','Influence'),('3','Influence and Control'))
    interestedparties=models.CharField(max_length=200,null=False, choices=INTERESTEDPARTIES)
    COMPANYINTERESTEDPARTIES=(('1','Control'),('2','Influence'),('3','Influence and Control'))
    companyinterestedparties=models.CharField(max_length=200,null=False, choices=INTERESTEDPARTIES)
    PRIORITIZING=(('1','P1'),('2','P2'),('3','P3'))
    priority=models.CharField(max_length=200,null=False, choices=PRIORITIZING,verbose_name='Priority:')
    ACTION=(('1','Training and awareness'),('2','Customer satisfaction survey'),('3','Performance monitoring'),('4','Service Level Management'),('5','Tax Compliance/Policing'),('6','Auditing'),('7','Contract management'),('8','Compliance reviews'),('9','Others'))
    actiontaken=models.CharField(max_length=200,null=False, verbose_name='Action to Manage IP:',choices=ACTION)
    actionOther=models.TextField(null=True,blank=True,verbose_name='Other, specify')
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, related_name='interested_entered_by',on_delete=models.SET_NULL)
    date_today=models.DateField("Date created:",default=datetime.now)
    due=models.DateField("When:", null=True)
    responsibility= models.ForeignKey('accounts.employees',on_delete=models.CASCADE,verbose_name='Responsibility:',related_name='IPresponsibility')
    status=models.ForeignKey(approval_status, on_delete=models.SET_NULL,null=True,verbose_name='Status:')
    rejected=models.TextField("Reason for rejecting:",null=True,blank=True, help_text='If rejected, please give a reason')
    approval_date=models.DateField("Date Approved:",null=True,blank=True)
    approved_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, related_name='IPApprov_by',on_delete=models.SET_NULL)
    def __str__(self):
        return self.ip_number

class department(models.Model):
    id=models.CharField("IP No.:",max_length=200,default="TEGA-IP-Q-"+car_no(),primary_key=True)
    name=models.TextField("DeptName:")
    faculty=models.TextField("Faculty:")

    def __str__(self):
        return self.id

class student(models.Model):
    id=models.CharField("ID.:",max_length=200,default="TEGA-IP-Q-"+car_no(),primary_key=True)
    name=models.TextField("Name:")
    departments=models.ForeignKey(department,on_delete=models.CASCADE,verbose_name='dept:')

class RequirementCategory(models.Model):
    cat_id=models.CharField("Category ID:",max_length=50,primary_key=True)
    cat_name=models.TextField("Description:")
    def __str__(self):
        return self.cat_name

class InterestedParties(models.Model):
    IP_id=models.CharField("Interested party ID:",max_length=50,primary_key=True)
    IP_name=models.TextField("Description:")
    def __str__(self):
        return self.IP_name

class mod9001_regulatoryReq(models.Model):
    regulatory_number=models.CharField("IP No.:",max_length=200,default="TEGA-IP-LRO-Q-"+car_no(),primary_key=True)
    registered=models.DateField("Date of registration:")
    analyst= models.ForeignKey('accounts.employees',on_delete=models.CASCADE,verbose_name='Lead Analyst:')
    cat_name=models.ForeignKey(RequirementCategory, on_delete=models.CASCADE,verbose_name='Requirement Category ID:',related_name='RequirementCategory')
    otherCategory=models.TextField("Other category:",null=True,blank=True)    
    description=models.TextField("Describe:",null=True,blank=True)
    document=models.TextField("Document Stipulating the Requirment:",null=True,blank=True)
    #interestedparty=models.ForeignKey(InterestedParties, on_delete=models.CASCADE,verbose_name='Interested Party ID:',related_name='interestedparty')
    parties=(('1','Customers'),('2','Regulators'),('3','Hardware/Equipment Suppliers'),('4','Traning providers'),('5','Security providers'),('6','Internet providers'),('7','Insurance providers'),('8','Auditors'),('9','Certification bodies'),('10','Inspectors'),('11','Business partners'),('12','Competitors'),('13','Neighbourhood'),('14','Local authorities'),('15','Family'),('16','Other'))
    interestedparty=models.CharField(max_length=200,null=True,blank=True, choices=parties)
   
    otherInterestedParty=models.TextField("Other interested party:",null=True,blank=True)
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, related_name='regulatoryreq_entered_by',on_delete=models.SET_NULL)
    date_today=models.DateField("Date created:",default=datetime.now)
    due=models.DateField("When:", null=True)
    responsibility= models.ForeignKey('accounts.employees',on_delete=models.CASCADE,verbose_name='Responsibility:',related_name='regulatoryresponsibility')
    status=models.ForeignKey(approval_status, on_delete=models.SET_NULL,null=True,verbose_name='Status:')
    rejected=models.TextField("Reason for rejecting:",null=True,blank=True, help_text='If rejected, please give a reason')
    approval_date=models.DateField("Date Approved:",null=True,blank=True)
    approved_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, related_name='reqApprov_by',on_delete=models.SET_NULL)


class contextdetails(models.Model):
    context_id=models.CharField("Risk Context ID:",max_length=50,primary_key=True)
    cont_desc=models.TextField("Description:")
    def __str__(self):
        return self.cont_desc

class risklikelihood(models.Model):
    likelihood_id=models.CharField("Risk likelihood ID:",max_length=50,primary_key=True)
    likelihood_desc=models.TextField("Description:")
    def __str__(self):
        return self.likelihood_desc

class riskseverity(models.Model):
    riskseverity_id=models.CharField("Risk Severity ID:",max_length=50,primary_key=True)
    riskseverity_desc=models.TextField("Description:")
    def __str__(self):
        return self.riskseverity_desc

class residuerisklikelihood(models.Model):
    likelihood_id=models.CharField("Risk likelihood ID:",max_length=50,primary_key=True)
    likelihood_desc=models.TextField("Description:")
    def __str__(self):
        return self.likelihood_desc

class residueriskseverity(models.Model):
    riskseverity_id=models.CharField("Risk Severity ID:",max_length=50,primary_key=True)
    riskseverity_desc=models.TextField("Description:")
    def __str__(self):
        return self.riskseverity_desc

class risktreat(models.Model):
    risk_desc=models.TextField("Description:")
    def __str__(self):
        return self.risk_desc

class riskmitigation(models.Model):
    risk_mitigation=models.TextField("Risk Mitigation:")
    def __str__(self):
        return self.risk_mitigation

class riskdesc(models.Model):
    risk_description=models.TextField("Risk description:")
    def __str__(self):
        return self.risk_description


class mod9001_risks(models.Model):
    risk_number=models.CharField("RISK No.:",max_length=200,default="TEGA-RA-"+car_no(),primary_key=True)
    risk_date=models.DateField("Date of analysis:")
    assessor= models.ForeignKey('accounts.employees',on_delete=models.CASCADE,verbose_name='Lead Assessor:',related_name='issuenumber')
    issue_number= models.ForeignKey(mod9001_issues,on_delete=models.CASCADE,verbose_name='Issue number:',null=True,blank=True)
    ip_number= models.ForeignKey(mod9001_interestedParties,on_delete=models.CASCADE,verbose_name='IP number:',null=True,blank=True)
 
    issue_description=models.TextField("Context Description:",null=True,blank=True)
    contextdetails=models.ForeignKey(contextdetails, on_delete=models.CASCADE,verbose_name='Context:',related_name='contextdetail')
    riskdescription=models.ForeignKey(riskdesc, on_delete=models.CASCADE,verbose_name='Risk Description:',related_name='riskdescription',null=True,blank=True)
    description=models.TextField("Risk Description:",null=True,blank=True)
    likelihood=models.ForeignKey(risklikelihood, on_delete=models.CASCADE,verbose_name='Risk likelihood:',related_name='risklikelihood',null=True,blank=True)
    severity=models.ForeignKey(riskseverity, on_delete=models.CASCADE,verbose_name='Risk Severity:',related_name='riskseverity',null=True,blank=True)
    riskrating=models.IntegerField("Risk Rating:",null=True,blank=True)
    riskrank=models.CharField("Risk category:",max_length=6,null=True,blank=True)

    residuelikelihood=models.ForeignKey(residuerisklikelihood, on_delete=models.CASCADE,verbose_name='Risk likelihood:',related_name='residuerisklikelihood',null=True, blank=True)
    residueseverity=models.ForeignKey(residueriskseverity, on_delete=models.CASCADE,verbose_name='Risk Severity:',related_name='residuerisklikelihood',null=True, blank=True)
    residueriskrating=models.IntegerField("Risk Rating:",null=True,blank=True)
    residueriskrank=models.CharField("Risk category:",max_length=6,null=True,blank=True)
    
    
    
    risktreatment=models.ForeignKey(risktreat, on_delete=models.CASCADE,verbose_name='Risk Treatment:',related_name='risktreatment',null=True,blank=True)
    retainreason=models.TextField("You chose retain, please give reason:",null=True,blank=True)
    riskmitigation=models.ForeignKey(riskmitigation, on_delete=models.CASCADE,verbose_name='Risk Mitigation:',related_name='riskmitigation',null=True,blank=True)

    
    mitigation=models.TextField("Other, please specify:",null=True,blank=True, help_text='Please describe other mitigation')
    mitigationdesc=models.TextField("Please describe if any:",null=True,blank=True, help_text='Please give risk mitigation details')
    
    evidence=models.TextField("Evidence of documented information:",null=True,blank=True)
    document = models.FileField("Please upload evidence",upload_to ='uploads/',null=True,blank=True)
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, related_name='risk_entered_by',on_delete=models.SET_NULL)
    date_today=models.DateField("Date created:",default=datetime.now)
    due=models.DateField("When:",null=True,blank=True)
    responsibility= models.ForeignKey('accounts.employees',on_delete=models.CASCADE,verbose_name='Responsibility:',related_name='riskresponsibility',null=True,blank=True)
    status=models.ForeignKey(approval_status, on_delete=models.SET_NULL,verbose_name='Status:',null=True,blank=True)
    rejected=models.TextField("Reason for rejecting:",null=True,blank=True, help_text='If rejected, please give a reason')
    approval_date=models.DateField("Date Approved:",null=True,blank=True)
    approved_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, related_name='risk_OPPApprov_by',on_delete=models.SET_NULL)
    record_type=models.TextField("Record Type:",null=True,blank=True, help_text='Specifies whether the record is risk or opprotunity entry')
    verification=models.ForeignKey(RISK_OPPverification, on_delete=models.SET_NULL,verbose_name='Verification:',null=True,blank=True)

    verification_status=models.CharField(max_length=200, null=True,blank=True)
    verification_failed=models.TextField("Reason for rejecting:",null=True,blank=True, help_text='If rejected, please give a reason')


        









    

    





  
    


















        




