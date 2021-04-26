from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from random import randint
from django import forms
from django.conf import settings


# Create your models here.
#FUNCTION TO AUTO GENERATE CAR NUMBER DDMMYYY & A RANDOM NUMBER BTN 100-3048####################################

   
######## RECORD IDs############################
def car_no():

    now = datetime.now()
    t=(now.strftime('%H'))+(now.strftime('%M'))+(now.strftime('%S'))

    return str((date.today()).strftime("%d%m%Y"))+str(randint(0, 999))




#############DEPARTMENT TABLE####################################
class Company(models.Model):
    company_code=models.CharField("Company Code:",max_length=6,primary_key=True)
    company_name=models.TextField("Company Name:")
    def __str__(self):
        return self.company_code

#############DEPARTMENT TABLE####################################
class Department(models.Model):
    dept_id=models.CharField("Department ID:",max_length=50,primary_key=True)
    dept_name=models.TextField("Name:")
    def __str__(self):
        return self.dept_name

############### NON CONFORMITY SOURCE LIST TABLE##################

#class car_NonConfSrc(models.Model):
#    non_conf_CHOICES=[('Iaudit','Internal audit'),('Eaudit','External audit'),('MgtRev','Management Review'),('Proc','Process non-conformity'),
# ('Sugg','Suggestion-improvement'),('Cust','Customer Complaint'),('Inci','Incident'),('Thrdpty','Third Party Complaint')]

#    nonconformity=models.CharField(max_length=50,choices=non_conf_CHOICES)

class NonConformitySource(models.Model):
    id=models.CharField("Non conformity ID.:",max_length=10,primary_key=True)
    description=models.CharField("Non Conformity",max_length=200,null=False, blank=False)
    def __str__(self):
        return self.description

## NON CONFORMITY LIST ##############
class NonConformityList(models.Model):
    source=models.ForeignKey(NonConformitySource,null=True,on_delete=models.SET_NULL,verbose_name=("Source"))
    description=models.CharField("Description.:",max_length=100)
    def __str__(self):
        return self.description

#CAR corrective or containment list

class NonConformityAction(models.Model):
    id=models.CharField("Non conformity ID.:",max_length=10,primary_key=True)
    description=models.CharField("Containment action", max_length=50,null=True,blank=True)
    def __str__(self):
        return self.description

class RootCause(models.Model):
    description=models.CharField("Root cause analysis", max_length=50,null=True,blank=True)
    def __str__(self):
        return self.description

class CorrectivePreventiveAction(models.Model):
    description=models.CharField("Proposed corrective or preventive Action", max_length=50,null=True,blank=True)
    def __str__(self):
        return self.description

class Carstatus(models.Model):

    description=models.CharField("CAR status", max_length=50,null=True,blank=True)
    def __str__(self):
        return self.description

class Carsverification(models.Model):

    description=models.CharField("CAR verification", max_length=50,null=True,blank=True)
    def __str__(self):
        return self.description

class CarPriority(models.Model):

    description=models.CharField("CAR Priority", max_length=50,null=True,blank=True)
    def __str__(self):
        return self.description
###################EMPLOYEES TITLES########################### 
class Employee_titles(models.Model):
    title_id=models.CharField("Title ID:",max_length=50,primary_key=True)
    title_name=models.TextField("Name:")
    def __str__(self):
        return self.title_name
######## TABLE EMPLOYEES ############################



class employees(models.Model):
    employeeID=models.CharField("Employee ID",max_length=10,primary_key=True,default="TEGA"+str(randint(0, 999)))
    title=models.ForeignKey(Employee_titles, on_delete=models.CASCADE,verbose_name='Title:',related_name='title',null=True,blank=True)
    registered=models.DateField("Reg. Date:")
    firstName=models.TextField("First Name",null=False,blank=True)
    lastName=models.TextField("Last Name",null=False,blank=False)
    email=models.EmailField("Email",blank=True,null=True,unique=True)
    dept=models.ForeignKey(Department, on_delete=models.CASCADE,verbose_name='Department:',related_name='employee')
    supervisor=models.ForeignKey(Employee_titles, on_delete=models.CASCADE,verbose_name='Supervisor:',related_name='reportsTo',null=True,blank=True)
    def __str__(self):
        return self.firstName









######Corrective Action Request###################
class car(models.Model):
    verification_status=(('Closed','Close'),('Rejected','Reject'))
    car_number=models.CharField("Corrective action no.:",max_length=200,default="TEGA"+car_no(),primary_key=True)
    car_dateoccur=models.DateField("Date of Occurence:",error_messages ={"unique":"The Geeks Field you enetered is not unique."})
    car_time=models.TimeField("Time:",default=datetime.now)
    car_dept=models.ForeignKey(Department, on_delete=models.CASCADE,verbose_name='Affected Department ID:',related_name='Department')
    car_userid= models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Reported by:')
    nonconf=models.ForeignKey(NonConformitySource,null=True, on_delete=models.SET_NULL)
    car_issue=models.TextField("Non conformity/Issue:",null=True,blank=True)
    description=models.TextField("Describe:",null=True,blank=True)    
    action=models.ForeignKey(NonConformityAction,null=True, on_delete=models.SET_NULL,verbose_name='Containment action',related_name='containmentaction')
   
    CAother=models.TextField("Specify Other:",null=True,blank=True, help_text='Specify other corrective/containment action')
    rootcause=models.ForeignKey(RootCause,null=True, on_delete=models.SET_NULL,verbose_name='Root Cause Analysis')
    Rootother=models.TextField("Specify Other:",null=True,blank=True, help_text='Specify other root cause')
    correctiveaction=models.ForeignKey(CorrectivePreventiveAction,null=True, on_delete=models.SET_NULL,verbose_name='Corrective/Preventive Action')
    correctiveactionOther=models.TextField("Specify Other:",null=True,blank=True, help_text='Specify other Proposed corrective/Preventive action')
    proposedby= models.ForeignKey(User,on_delete=models.CASCADE,related_name='proposedby_user',verbose_name='Proposed by')
    proposedDate=models.DateField("CA/PA proposal Date:", null=False,blank=False)
    implementedby= models.ForeignKey(User,on_delete=models.CASCADE,related_name='implementedby_user',verbose_name='Implemented by')
    deadline=models.DateField("Implementation Deadline:", null=False,blank=False)
    car_date=models.DateField("Date created:",default=datetime.now)
    status=models.ForeignKey(Carstatus, on_delete=models.SET_NULL,null=True,verbose_name='CAR status:')
    verification=models.ForeignKey(Carsverification, on_delete=models.SET_NULL,null=True,verbose_name='CAR verification:')
    verification_status=models.CharField(max_length=200,null=True, choices=verification_status)
    verification_failed=models.TextField("Reason for rejecting:",null=True,blank=True, help_text='If rejected, please give a reason')


    priority=models.ForeignKey(CarPriority, on_delete=models.SET_NULL,null=True,verbose_name='CAR Priority:')
    rejected=models.TextField("Reason for rejecting:",null=True,blank=True, help_text='If rejected, please give a reason')
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, related_name='entered_by',on_delete=models.SET_NULL)
    entered_by=models.TextField("Entered by:",null=True,blank=True)

    def get_year(self):
        x=self.car_dateoccur.year
        return x



    
    def __str__(self):
        return self.car_number


#class carStatus(models.Model):
#    status_CHOICES=(('Open','Open'),('Closed','Closed'),('Approved','Approved'),('Rejected','Rejected'),('Pending','Pending'))
 #   car_number=models.ForeignKey(car,null=True, verbose_name=("CAR ID"), on_delete=models.CASCADE)
  #  car_status=models.CharField(("Status"), max_length=50,choices=status_CHOICES)

   # def __str__(self):
    #    return self.car_status


#create a product model
class Customer(models.Model):
    name=models.CharField(max_length=200,null=True)
    phone=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name
#many to many relations table tags
class Tag(models.Model):
    name=models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY=(('Indoor','Indoor'),('Out door','Out door'))
    name=models.CharField(max_length=200,null=True)
    price=models.FloatField(null=True)
    category=models.CharField(max_length=200,null=True, choices=CATEGORY)
    description=models.CharField(max_length=200,null=True, blank=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    tags=models.ManyToManyField(Tag)

    def __str__(self):
        return self.name
    



class Order(models.Model):

    STATUS=(('Pending','Pending'),
    ('Out of stock','Out of stock'),
    ('Delivered','Delivered'))

    customer=models.ForeignKey(Customer,null=True, on_delete=models.SET_NULL)
    product=models.ForeignKey(Product,null=True, on_delete=models.SET_NULL)
    status=models.CharField(max_length=200,null=True, choices=STATUS)
    date_created=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.product.name

class Passenger(models.Model):
    name = models.CharField(max_length=200)
    sex = models.CharField(max_length=200)
    survived = models.BooleanField()
    age = models.FloatField()
    ticket_class = models.PositiveSmallIntegerField()
    embarked = models.CharField(max_length=200)