from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from issues_9001.models import *
from operations_9001.models import *
from itsms_20000.models import *
from. forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout, update_session_auth_hash
from django.contrib.auth import get_user_model
from .decorators import unauthenticated_user,allowed_users
from .filters import CarFilter
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
import json
from django.db.models import Count, Q
import xlwt
from django.contrib.auth.models import User
from xlutils.copy import copy # http://pypi.python.org/pypi/xlutils
from xlrd import open_workbook # http://pypi.python.org/pypi/xlrd
import os
import csv
from .utils import *
from django.contrib.auth.models import Group
from django import template


register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name): 
    group = Group.objects.get(name=group_name) 
    return True if group in user.groups.all() else False
  

#function to get cars with 7 days to expire
def get_7days_expire(*x):
    date_str = x[0]
    date_object = datetime.strptime(date_str, '%m/%d/%Y').date()
    delta =date.today() - date_object 
    return delta.days



#@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def home(request):

    #################THIS CODE LOADS ALL PENDING TASKS BASED ON USER ACCOUNT######################################
    

    #if is_ManagementRepresentative(request.user):
    total_IPS= mod9001_interestedParties.objects.all().filter(status='5').count()
    total_IPS_rejected= mod9001_interestedParties.objects.all().filter(analyst_user_id=request.user.id).filter(date_today__gte=datetime.now() - timedelta(days=7)).filter(status='4').count()
    
    total_ISSUES= mod9001_issues.objects.all().filter(status='5').count()
    total_ISSUES_rejected= mod9001_issues.objects.all().filter(analyst_user_id=request.user.id).filter(date_today__gte=datetime.now() - timedelta(days=7)).filter(status='4').count()

    total_COMPLAINCE= mod9001_regulatoryReq.objects.all().filter(status='5').count()       
    total_COMPLAINCE_rejected=mod9001_regulatoryReq.objects.all().filter(analyst_user_id=request.user.id).filter(date_today__gte=datetime.now() - timedelta(days=7)).filter(status='4').count()
 
    total_RISKS= mod9001_risks.objects.all().filter(status='5',record_type='RISK').filter(~Q(verification_status='Closed')).count()
    total_RISKS_pending= mod9001_risks.objects.all().filter(record_group=my_data_group(request.user)).filter(due__gte=datetime.now() - timedelta(days=7)).filter(record_type='RISK').filter(status='1').filter(~Q(verification_status='Closed')).filter(record_group=my_data_group(request.user)).count()

    total_OPPORTUNITY= mod9001_risks.objects.all().filter(record_type='OPP').filter(status='5').filter(~Q(verification_status='Closed')).count()
    total_OPPORTUNITY_pending= mod9001_risks.objects.all().filter(record_group=my_data_group(request.user)).filter(due__gte=datetime.now() - timedelta(days=7)).filter(record_type='OPP').filter(status='1').filter(~Q(verification='1')).filter(record_group=my_data_group(request.user)).count()

    
    total_INCIDENTREGISTER=mod9001_incidentregister.objects.filter(analysis_flag='No').filter(record_group=my_data_group(request.user)).count()
    total_INCIDENTREGISTER_rejected= mod9001_incidentregisterStaff.objects.all().filter(date_today__gte=datetime.now() - timedelta(days=7)).filter(qmsstatus='3').count()
    total_INCIDENTREGISTER_pending= mod9001_incidentregisterStaff.objects.all().filter(due__gte=datetime.now() - timedelta(days=7)).filter(~Q(qmsstatus='3')).filter(~Q(qmsstatus='1')).filter(record_group=my_data_group(request.user)).count()
        
       
    total_CHANGEREQUEST= mod9001_changeRegister.objects.all().filter(status='5').count()
    total_CHANGEREQUEST_rejected= mod9001_changeRegister.objects.all().filter(raisedby_user_id=request.user.id).filter(date_today__gte=datetime.now() - timedelta(days=7)).filter(status='4').count()
    
    total_CUSTOMERSATISFACTION= mod9001_customerSatisfaction.objects.all().filter(status='1').filter(start__isnull=True).filter(record_group=my_data_group(request.user)).count()
    total_CUSTOMERSATISFACTION_rejected= mod9001_customerSatisfaction.objects.all().filter(date_today__gte=datetime.now() - timedelta(days=7)).filter(qmsstatus='3').count()
    total_CUSTOMERSATISFACTION_pending= mod9001_customerSatisfaction.objects.all().filter(due__gte=datetime.now() - timedelta(days=7)).filter(~Q(qmsstatus='3')).filter(~Q(qmsstatus='1')).filter(record_group=my_data_group(request.user)).count()     
    #total_CUSTOMERSATISFACTION_pending= mod9001_customerSatisfaction.objects.all().filter(due__gte=datetime.now() - timedelta(days=7)).filter(~Q(qmsstatus='3')).filter(~Q(qmsstatus='1'))
    
           #total_CUSTOMERCOMPLAINT= mod9001_customerComplaint.objects.all().filter(status='1').filter(~Q(qmsstatus='1')).count()      
    
    
    total_CUSTOMERCOMPLAINT= mod9001_customerComplaint.objects.filter(analysis_flag='No').filter(record_group=my_data_group(request.user)).count()   
    total_CUSTOMERCOMPLAINT_rejected= mod9001_customerComplaint.objects.all().filter(date_today__gte=datetime.now() - timedelta(days=7)).filter(qmsstatus='3').count()          
    total_CUSTOMERCOMPLAINT_pending= mod9001_customerComplaint.objects.all().filter(due__gte=datetime.now() - timedelta(days=7)).filter(~Q(qmsstatus='3')).filter(~Q(qmsstatus='1')).filter(record_group=my_data_group(request.user)).count()       

        #total_PROVIDERASSESSMENT= mod9001_providerassessment.objects.all().filter(status='1').filter(~Q(qmsstatus='1')).count()      
    total_PROVIDERASSESSMENT= mod9001_providerassessment.objects.all().filter(status='1').filter(qmsstatus__isnull=True).count()
    total_PROVIDERASSESSMENT_rejected= mod9001_providerassessment.objects.all().filter(date_today__gte=datetime.now() - timedelta(days=7)).filter(qmsstatus='3').count() 
    total_PROVIDERASSESSMENT_pending= mod9001_providerassessment.objects.all().filter(due__gte=datetime.now() - timedelta(days=7)).filter(~Q(qmsstatus='3')).filter(~Q(qmsstatus='1')).filter(record_group=my_data_group(request.user)).count() 
 
    total_TRAININGevaluation= mod9001_trainingregister.objects.all().filter(status='1').filter(qmsstatus__isnull=True).count()
    total_TRAININGevaluation_rejected= mod9001_trainingregister.objects.all().filter(date_today__gte=datetime.now() - timedelta(days=7)).filter(qmsstatus='3').count() 
    total_TRAININGevaluation_pending= mod9001_trainingregister.objects.all().filter(completion_date__gte=datetime.now() - timedelta(days=7)).filter(~Q(qmsstatus='3')).filter(~Q(qmsstatus='1')).filter(record_group=my_data_group(request.user)).count() 
    

    total_ServiceRequests= mod20000_service_request.objects.filter(planning_flag='No').filter(record_group=my_data_group(request.user)).count()
    total_ServiceRequests_rejected= mod20000_service_planning.objects.all().filter(date_today__gte=datetime.now() - timedelta(days=7)).filter(qmsstatus='3').count()
    total_ServiceRequests_pending= mod20000_service_planning.objects.all().filter(due__gte=datetime.now() - timedelta(days=7)).filter(~Q(qmsstatus='3')).filter(~Q(qmsstatus='1')).filter(record_group=my_data_group(request.user)).count()
    


    

    if is_Executive(request.user):

        total_ServiceRequests_pending=0 
        total_TRAININGevaluation_pending=0 
        total_PROVIDERASSESSMENT_pending=0 
        total_CUSTOMERSATISFACTION_pending=0 
        total_RISKS_pending=0
        total_OPPORTUNITY_pending=0 
        total_QMSplanner_pending=0
        total_Trainingplanner_pending=0 
        total_INCIDENTREGISTER_pending=0 
        total_CORRECTIVEACTION_pending=0
        total_CUSTOMERCOMPLAINT_pending=0
        total_CORRECTIVEACTION_pending_planning=0
        total_ServiceRequests=0
        total_CUSTOMERCOMPLAINT=0
        total_INCIDENTREGISTER=0

        total_QMSplanner= mod9001_qmsplanner.objects.all().filter(status='5').filter(planner_user_title=20).count()
        #total_QMSplanner_rejected= mod9001_qmsplanner.objects.all().filter(planner_user_id=request.user.id).filter(date_today__gte=datetime.now() - timedelta(days=7)).filter(status='4').count()
        #total_QMSplanner_pending= mod9001_qmsplanner.objects.all().filter(end__gte=datetime.now() - timedelta(days=7)).filter(status='1').filter(~Q(qmsstatus=1)).filter(~Q(qmsstatus=3)).count()
        total_QMSplanner_rejected=0
        total_QMSplanner_pending=0
        total_Trainingplanner= mod9001_trainingplanner.objects.all().filter(status='5').filter(planner_user_title=20).count()
        #total_Trainingplanner_rejected= mod9001_trainingplanner.objects.all().filter(planner_user_id=request.user.id).filter(date_today__gte=datetime.now() - timedelta(days=7)).filter(status='4').count()      
        #total_Trainingplanner_pending= mod9001_trainingplanner.objects.all().filter(end__gte=datetime.now() - timedelta(days=7)).filter(status='1').filter(trainplannerstatus__isnull=True).count()
        total_Trainingplanner_rejected=0
        total_Trainingplanner_pending=0

        
        total_CORRECTIVEACTION_rejected=0
        total_CORRECTIVEACTION_pending_planning=0
        total_CORRECTIVEACTION= mod9001_planning.objects.all().filter(status='5').filter(planner_user_title=20).count()

    else:
        total_QMSplanner= mod9001_qmsplanner.objects.all().filter(status='5').filter(record_group=my_data_group(request.user)).filter(~Q(planner_user_title=20)).count() #exclude HOD entries
        total_QMSplanner_rejected= mod9001_qmsplanner.objects.all().filter(planner_user_id=request.user.id).filter(date_today__gte=datetime.now() - timedelta(days=7)).filter(status='4').count()
        total_QMSplanner_pending= mod9001_qmsplanner.objects.all().filter(end__gte=datetime.now() - timedelta(days=7)).filter(status='1').filter(~Q(qmsstatus=1)).filter(~Q(qmsstatus=3)).filter(record_group=my_data_group(request.user)).count()

        total_Trainingplanner= mod9001_trainingplanner.objects.all().filter(status='5').filter(record_group=my_data_group(request.user)).filter(~Q(planner_user_title=20)).count() #exclude HOD entries
        total_Trainingplanner_rejected= mod9001_trainingplanner.objects.all().filter(planner_user_id=request.user.id).filter(date_today__gte=datetime.now() - timedelta(days=7)).filter(status='4').count()      
        total_Trainingplanner_pending= mod9001_trainingplanner.objects.all().filter(end__gte=datetime.now() - timedelta(days=7)).filter(status='1').filter(trainplannerstatus__isnull=True).filter(record_group=my_data_group(request.user)).count()

        total_CORRECTIVEACTION_rejected= mod9001_planning.objects.all().filter(proposedby_user_id=request.user.id).filter(date_today__gte=datetime.now() - timedelta(days=7)).filter(status='4').count()
        total_CORRECTIVEACTION= mod9001_planning.objects.all().filter(status='5').filter(record_group=my_data_group(request.user)).filter(~Q(planner_user_title=20)).count()
        #total_CORRECTIVEACTION= mod9001_planning.objects.all().filter(status='5').filter(record_group=my_data_group(request.user))
        
        total_CORRECTIVEACTION_pending= mod9001_planning.objects.all().filter(due__gte=datetime.now() - timedelta(days=7)).filter(status='1').filter(~Q(qmsstatus='3')).filter(~Q(qmsstatus='1')).filter(record_group=my_data_group(request.user)).count()  
        total_CORRECTIVEACTION_pending_planning= mod9001_correctiveaction.objects.filter(car_flag='No').filter(record_group=my_data_group(request.user)).count()  
                
        
        
        
        
        
        total_IPS=0 
        total_ISSUES=0 
        total_COMPLAINCE=0 
        total_RISKS=0 
        total_OPPORTUNITY=0 
        #total_CORRECTIVEACTION=0
        total_CHANGEREQUEST=0
    
    
    
    
    total_tasks=total_CORRECTIVEACTION_pending_planning + total_TRAININGevaluation + total_ServiceRequests + total_IPS + total_ISSUES + total_COMPLAINCE + total_RISKS + total_OPPORTUNITY + total_QMSplanner + total_Trainingplanner + total_INCIDENTREGISTER + total_CORRECTIVEACTION + total_CHANGEREQUEST + total_CUSTOMERSATISFACTION + total_CUSTOMERCOMPLAINT + total_PROVIDERASSESSMENT
    total_tasks_pending= total_TRAININGevaluation_pending + total_ServiceRequests_pending  + total_RISKS_pending + total_OPPORTUNITY_pending + total_QMSplanner_pending + total_Trainingplanner_pending + total_INCIDENTREGISTER_pending + total_CORRECTIVEACTION_pending  + total_CUSTOMERSATISFACTION_pending + total_CUSTOMERCOMPLAINT_pending + total_PROVIDERASSESSMENT_pending
    total_tasks_rejected= total_IPS_rejected + total_ISSUES_rejected + total_COMPLAINCE_rejected  + total_QMSplanner_rejected + total_Trainingplanner_rejected + total_CORRECTIVEACTION_rejected + total_CHANGEREQUEST_rejected
 
    #########################CALCULATED ENVELOP TASKS BY USER GROUP#############################################
    
    TopManager_Tasks = total_IPS + total_ISSUES + total_COMPLAINCE + total_RISKS + total_OPPORTUNITY + total_QMSplanner + total_Trainingplanner +  total_CORRECTIVEACTION + total_CHANGEREQUEST + total_CUSTOMERSATISFACTION
    Auditor_Tasks = total_CUSTOMERCOMPLAINT_pending + total_ServiceRequests_pending + total_TRAININGevaluation_pending + total_PROVIDERASSESSMENT_pending + total_CUSTOMERSATISFACTION_pending + total_RISKS_pending + total_OPPORTUNITY_pending + total_QMSplanner_pending + total_Trainingplanner_pending + total_INCIDENTREGISTER_pending + total_CORRECTIVEACTION_pending
    Analyst_Tasks = total_INCIDENTREGISTER + total_CUSTOMERCOMPLAINT + total_ServiceRequests
    AnalystTopManagerAuditor_Tasks=TopManager_Tasks + Auditor_Tasks + Analyst_Tasks
    AnalystTopManager_Tasks= TopManager_Tasks + Analyst_Tasks
    AnalystAuditor_Tasks = Auditor_Tasks + Analyst_Tasks
    TopManagerAuditor_Tasks= TopManager_Tasks + Auditor_Tasks
    ExecutiveTasks= total_CORRECTIVEACTION + total_IPS + total_ISSUES + total_COMPLAINCE + total_RISKS + total_OPPORTUNITY + total_QMSplanner + total_Trainingplanner  + total_CHANGEREQUEST + total_CUSTOMERSATISFACTION
    #####################################END################################     
    
    #if total_tasks==0:
    #    total_tasks=''
    #total_tasks=total_TRAININGevaluation + total_ServiceRequests + total_IPS + total_ISSUES + total_COMPLAINCE + total_RISKS + total_OPPORTUNITY + total_QMSplanner + total_Trainingplanner + total_INCIDENTREGISTER + total_CORRECTIVEACTION + total_CORRECTIVEACTION_pending_planning + total_CHANGEREQUEST + total_CUSTOMERSATISFACTION + total_CUSTOMERCOMPLAINT + total_PROVIDERASSESSMENT
    tasks=total_tasks+total_tasks_pending
    if tasks==0:
        tasks=''
    #request.session['total_tasks'] = total_tasks
    #print("RISKS PENDING",total_RISKS_pending) 
    #print("total_tasks PENDING",total_tasks)  
    #print("Auditor_Tasks PENDING",Auditor_Tasks) 
#####################END##################################

 ##################BAR CHART###########################
    total_IPS_created= mod9001_interestedParties.objects.all().count()
    total_IPS_approved= mod9001_interestedParties.objects.all().filter(status='1').count()

    total_ISSUES_created= mod9001_issues.objects.all().count()
    total_ISSUES_approved= mod9001_issues.objects.all().filter(status='1').count()

    total_COMPLAINCE_created= mod9001_regulatoryReq.objects.all().count()
    total_COMPLAINCE_approved= mod9001_regulatoryReq.objects.all().filter(status='1').count()
       
    total_RISKS_created= mod9001_risks.objects.all().filter(record_type='RISK').count()
    total_RISKS_approved= mod9001_risks.objects.all().filter(status='1').filter(record_type='RISK').count()
    total_RISKS_verified= mod9001_risks.objects.all().filter(status='5').filter(record_type='RISK').filter(verification='2').count()
    total_RISKS_completed= mod9001_risks.objects.all().filter(status='1').filter(record_type='RISK').filter(verification_status='Closed').count()
    
    total_OPPORTUNITY_created= mod9001_risks.objects.all().filter(record_type='OPP').count()
    total_OPPORTUNITY_approved= mod9001_risks.objects.all().filter(status='1').filter(record_type='OPP').count()
    #print("total_OPPORTUNITY_approved: ",total_OPPORTUNITY_approved)
    total_OPPORTUNITY_verified= mod9001_risks.objects.all().filter(status='5').filter(record_type='OPP').filter(verification='2').count()
    total_OPPORTUNITY_completed= mod9001_risks.objects.all().filter(status='1').filter(record_type='OPP').filter(verification_status='Closed').count()
    
    total_QMSplanner_created= mod9001_qmsplanner.objects.all().count()
    total_QMSplanner_approved= mod9001_qmsplanner.objects.all().filter(status='1').count()
    total_QMSplanner_verified= mod9001_qmsplanner.objects.all().filter(status='1').filter(verification='2').count()
    total_QMSplanner_completed= mod9001_qmsplanner.objects.all().filter(status='1').filter(verification_status='Closed').count()

    
    total_Trainingplanner_created= mod9001_trainingplanner.objects.all().count()
    total_Trainingplanner_approved= mod9001_trainingplanner.objects.all().filter(status='1').count()
    total_Trainingplanner_verified= mod9001_trainingplanner.objects.all().filter(status='1').filter(verification='2').count()
    total_Trainingplanner_completed= mod9001_trainingplanner.objects.all().filter(status='1').filter(verification_status='Closed').count()
 
    total_INCIDENTREGISTER_created= mod9001_incidentregisterStaff.objects.all().count()
    total_INCIDENTREGISTER_approved= mod9001_incidentregisterStaff.objects.all().filter(status='1').count()
    total_INCIDENTREGISTER_verified= mod9001_incidentregisterStaff.objects.all().filter(status='1').filter(verification='2').count()
    total_INCIDENTREGISTER_completed= mod9001_incidentregisterStaff.objects.all().filter(status='1').filter(verification_status='Closed').count()
    
    total_CORRECTIVEACTION_created= mod9001_planning.objects.all().count()
    total_CORRECTIVEACTION_approved= mod9001_planning.objects.all().filter(status='1').count()
    total_CORRECTIVEACTION_verified= mod9001_planning.objects.all().filter(status='1').filter(verification='2').count()
    total_CORRECTIVEACTION_completed= mod9001_planning.objects.all().filter(status='1').filter(verification_status='Closed').count()
    
    total_CHANGEREQUEST_created= mod9001_changeRegister.objects.all().count()
    total_CHANGEREQUEST_approved= mod9001_changeRegister.objects.all().filter(status='1').count()
    total_CHANGEREQUEST_verified= mod9001_changeRegister.objects.all().filter(status='1').filter(verification='2').count()
    total_CHANGEREQUEST_completed= mod9001_changeRegister.objects.all().filter(status='1').filter(verification_status='Closed').count()


    total_CUSTOMERSATISFACTION_created= mod9001_customerSatisfaction.objects.all().count()            
    total_CUSTOMERSATISFACTION_approved= mod9001_customerSatisfaction.objects.all().filter(status='1').count()            
    total_CUSTOMERSATISFACTION_verified= mod9001_customerSatisfaction.objects.all().filter(status='1').filter(verification='2').count()            
    total_CUSTOMERSATISFACTION_completed= mod9001_customerSatisfaction.objects.all().filter(status='1').filter(verification_status='Closed').count()           
     
    
    total_CUSTOMERCOMPLAINT_created= mod9001_customerComplaint.objects.all().filter(status='1').filter(~Q(qmsstatus='1')).count()      
    total_CUSTOMERCOMPLAINT_approved= mod9001_customerComplaint.objects.all().filter(status='1').count()            
    total_CUSTOMERCOMPLAINT_verified= mod9001_customerComplaint.objects.all().filter(status='1').filter(verification='2').count()            
    total_CUSTOMERCOMPLAINT_completed= mod9001_customerComplaint.objects.all().filter(status='1').filter(verification_status='Closed').count()           
         
    total_PROVIDERASSESSMENT_created= mod9001_providerassessment.objects.all().count()      
    total_PROVIDERASSESSMENT_approved= mod9001_providerassessment.objects.all().filter(status='1').count()      
    total_PROVIDERASSESSMENT_verified= mod9001_providerassessment.objects.all().filter(status='1').filter(verification='2').count()     
    total_PROVIDERASSESSMENT_completed= mod9001_providerassessment.objects.all().filter(status='1').filter(verification_status='Closed').count()             


 #####################END##########################












    
    ######## RECENT 5 RISKS/OPPORTUNITIES #########
    carstatus=mod9001_risks.objects.all().filter(~Q(verification_status='Closed')).order_by('risk_date')[0:5] #get top 5 risksand opportuninities pending 
    ##########END############
    total_jobs_created=total_IPS_created + total_ISSUES_created + total_COMPLAINCE_created + total_RISKS_created + total_OPPORTUNITY_created + total_QMSplanner_created + total_Trainingplanner_created + total_INCIDENTREGISTER_created + total_CORRECTIVEACTION_created + total_CHANGEREQUEST_created + total_CUSTOMERSATISFACTION_created + total_CUSTOMERCOMPLAINT_created + total_PROVIDERASSESSMENT_created
    total_jobs_completed=total_IPS_approved + total_ISSUES_approved + total_COMPLAINCE_approved + total_RISKS_completed + total_OPPORTUNITY_completed + total_QMSplanner_completed + total_Trainingplanner_completed + total_INCIDENTREGISTER_completed + total_CORRECTIVEACTION_completed +  total_CHANGEREQUEST_completed + total_CUSTOMERSATISFACTION_completed + total_CUSTOMERCOMPLAINT_completed + total_PROVIDERASSESSMENT_completed    
    total_jobs_pending=total_jobs_created - total_jobs_completed
    
    
    cars=car.objects.all()
    customers=Customer.objects.all()
    ################################################################
    total_cars=total_tasks
    total_approved=total_tasks
    total_pending=total_tasks
    #dump=ticket_class_view_3()
    carExpire7days=car.objects.filter(status=4).filter(~Q(verification=1)) #cars with  Status Open 
    #count=0

##########################################################################

    #for i in carstatus:

        

#############################################################################
    counts=0
    due=0
    for i in carExpire7days:
        w=i.deadline
        t=w.strftime('%m/%d/%Y')
        if get_7days_expire(t)<8 and get_7days_expire(t)>=0:
            counts+=1
        if get_7days_expire(t)<0:
            due+=1

###################NUMBER OF INCIDENTS#############################################
    incidents=mod9001_incidentregisterStaff.objects.all()
    
    a=0 #one
    b=0 #two
    c=0 #three
    d=0 #four
    e=0 #five
    f=0 #six
    ####### variables g to l will contain incident cost figures #######
    g=0 #seven
    h=0 #eight
    m=0 #nine
    j=0 #ten
    k=0 #eleven
    l=0 #twelve

    for i in incidents:
        if i.incident_number is not None:
            
            w=i.incident_number.date
            t=w.strftime('%m/%d/%Y')
        #print("printing dates",t)
        #print("printing dates ranges",get_7days_expire(t))
            if get_7days_expire(t)<=30 and get_7days_expire(t)>=0:
                a+=1
                if i.costdescription is not None:
                    g+=i.costdescription
            
            #print("printing cost",g, i.costdescription)
            
            elif get_7days_expire(t)>30 and get_7days_expire(t)<=60:
                b+=1
                if i.costdescription is not None:
                    h+=i.costdescription
            #print("printing cost",h, i.costdescription)
            elif get_7days_expire(t)>60 and get_7days_expire(t)<=90:
                c+=1
                if i.costdescription is not None:
                    m+=i.costdescription
            #print("printing cost",i, i.costdescription)
            elif get_7days_expire(t)>90 and get_7days_expire(t)<=120:
                d+=1
                if i.costdescription is not None:
                    j+=i.costdescription
            #print("printing cost",j, i.costdescription)
            elif get_7days_expire(t)>120 and get_7days_expire(t)<=150:
                e+=1
                if i.costdescription is not None:
                    k+=i.costdescription
            #print("printing cost",k, i.costdescription)
            elif get_7days_expire(t)>150 and get_7days_expire(t)<=180:
                f+=1
                if i.costdescription is not None:
                    l+=i.costdescription
            #print("printing cost",l, i.costdescription)
            else:
                pass

    #print("PRINTING MONTHS", a, b, c, d , e ,f )




#################################END############################################

###################NUMBER OF INCIDENTS#############################################
    incidents=mod9001_incidentregister.objects.all()
    customer_complaint=mod9001_customerComplaint.objects.all()
    aa=0 #one
    bb=0 #two
    cc=0 #three
    dd=0 #four
    ee=0 #five
    ff=0 #six
   

    for i in customer_complaint:
        w=i.date
        t=w.strftime('%m/%d/%Y')
        if get_7days_expire(t)<=30 and get_7days_expire(t)>=0:
            aa+=1
        elif get_7days_expire(t)>30 and get_7days_expire(t)<=60:
            bb+=1
        elif get_7days_expire(t)>60 and get_7days_expire(t)<=90:
            cc+=1
        elif get_7days_expire(t)>90 and get_7days_expire(t)<=120:
            dd+=1
        elif get_7days_expire(t)>120 and get_7days_expire(t)<=150:
            ee+=1
        elif get_7days_expire(t)>150 and get_7days_expire(t)<=180:
            ff+=1
        else:
            pass

    #print("PRINTING MONTHS aa bb cc dd ee ff ", aa, bb, cc, dd , ee ,ff )




###########################################################################

    categories = ['IPs','Issues','Compliance','Risks','Opportunity','QMSplanner','TrainingPlanner','Incident','CorrectiveAction','ChangeRequest','CustomerSatisfaction','CustomerComplaint','ProviderAssesment']
    #survived_series_data = [total_pending,total_approved,12]
    #not_survived_series_data = [78,50,31]
        
    

    Created = {
        'name': 'Created',
        'data': [total_IPS_created,total_ISSUES_created,total_COMPLAINCE_created,total_RISKS_created,total_OPPORTUNITY_created,total_QMSplanner_created,total_Trainingplanner_created,total_INCIDENTREGISTER_created,total_CORRECTIVEACTION_created,total_CHANGEREQUEST_created,total_CUSTOMERSATISFACTION_created,total_CUSTOMERCOMPLAINT_created,total_PROVIDERASSESSMENT_created],
        'color': 'green'
    }
    Approved= {
        'name': 'Approved',
        'data': [total_IPS_approved,total_ISSUES_approved,total_COMPLAINCE_approved,total_OPPORTUNITY_approved,total_QMSplanner_approved,total_Trainingplanner_approved,total_INCIDENTREGISTER_approved,total_CORRECTIVEACTION_approved,total_CHANGEREQUEST_approved,total_CUSTOMERSATISFACTION_approved,total_CUSTOMERCOMPLAINT_approved,total_PROVIDERASSESSMENT_approved],
        'color': 'red'
    }

    Verified = {
        'name': 'verified',
        'data': [0,0,0,total_RISKS_verified,total_OPPORTUNITY_verified,total_QMSplanner_verified,total_Trainingplanner_verified,total_INCIDENTREGISTER_verified,total_CORRECTIVEACTION_verified,total_CHANGEREQUEST_verified,total_CUSTOMERSATISFACTION_verified,total_CUSTOMERCOMPLAINT_verified,total_PROVIDERASSESSMENT_verified],
        'color': 'blue'
    }

    Completed = {
        'name': 'Completed',
        'data': [0,0,0,total_RISKS_created,total_OPPORTUNITY_completed,total_QMSplanner_completed,total_Trainingplanner_completed,total_INCIDENTREGISTER_completed,total_CORRECTIVEACTION_completed,total_CHANGEREQUEST_completed,total_CUSTOMERSATISFACTION_completed,total_CUSTOMERCOMPLAINT_completed,total_PROVIDERASSESSMENT_completed],
        'color': 'yellow'
    }
    
  

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Tasks by status'},
        'credits': 'false',
       
        'xAxis': {'categories': categories},
        'series': [Created,Approved,Verified,Completed],
           
    }
 
    
    Created2 = {
        'name': 'Created',
        'data':[76,34,87],
        #'data': list(map(lambda row: {'name': 'Created', 'y': row[12]})),
        #'data': [{'name': 'Chrome Mobile', y: 4}, {'name': 'Chrome', y: 9}],

        'color': ''
    }
 ################NON CONFORMITY BAR CHART#################################
    
    nonconf=mod9001_planning.objects.all()
    nonconf2=list(nonconf)
    #print("printing querysetlist",nonconf2)
    process=[]
    finding=[]
    

    
    
    if nonconf.count() > 0:
        for i in nonconf:
            
            process.append(i.car_no.process)
            finding.append(i.car_no.finding)

    #print(process)
    #print(finding)
    nonconfs = {
        'name': 'nonconfs',
        'data':finding,
        'color': ''
    }
    nonconfcharts = {
        'chart': {'type': 'column'},
        'title': {'text': 'Non Conformity'},
        'xAxis': {'process': process},
        'series': [nonconfs],
        
    }

    #print("printing processes",process)
   
       
    charts = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Customer Satisfaction Survey'},
        'xAxis': {'categories': categories},
        'series': [Created2],
        
    }
    #print("printing categories",categories)
    dump = json.dumps(chart)
    dump2=json.dumps(charts)
    #dump3=json.dumps(nonconfcharts)
    browser_stats = [('Chrome', 52.9), ('Firefox', 27.7), ('Opera', 1.6),
                 ('Internet Explorer', 12.6), ('Safari', 4)]


    
    ################PIE CHART DATA FOR RESIDUAL RISKS#################################
    residual_risks=mod9001_risks.objects.all()

    low=0 #Low
    high=0 #High
    medium=0 #Medium


    for i in residual_risks:
        if i.residueriskrank=='Low':
            low+=1
        elif i.residueriskrank=='High':
            high+=1
        elif i.residueriskrank=='Medium':
            medium+=1
        else:
            pass









    
    ################PIE CHART DATA FOR CUSTOMER SATISFACTION SURVEY#################################
    customer_survey=mod9001_customerSatisfaction.objects.all()

    w=0 #poor
    x=0 #improvement
    y=0 #satisfactory
    z=0 #good
    s=0 #excellent

    for i in customer_survey:
        if i.rankdesc_survey=='Poor':
            w+=1
        elif i.rankdesc_survey=='Improvement':
            x+=1
        elif i.rankdesc_survey=='Satisfactory':
            y+=1
        elif i.rankdesc_survey=='Good':
            z+=1
        elif i.rankdesc_survey=='Excellent':
            s+=1
        else:
            pass

     #############################NON CONFORMITY GRAPH FOR CORRECTIVE ACTION REGISTER##########################################################      
    correctiveaction= mod9001_correctiveaction.objects.all().filter(finding='1')
    BidManagement=0
    IToperations=0
    InternalAuditing=0
    AccountsReceivables=0
    AccountsPayables=0
    Recruitment=0
    Training=0
    Management=0
    Procurement=0
    Projects=0
    TechnicalSupport=0
    CustomerSatisfaction=0    
    Marketing=0
    Administration=0


    if correctiveaction.count() > 0:
        for i in correctiveaction:
            if str(i.process)=='Bid Management':
                BidManagement+=1
            elif str(i.process)=='IT Operations':
                IToperations+=1
            elif str(i.process)=='Internal Auditing':
                InternalAuditing+=1       
            elif str(i.process)=='Accounts Receivables':
                AccountsReceivables+=1
            elif str(i.process)=='Accounts Payables':
                AccountsPayables+=1           
            elif str(i.process)=='Recruitment':
                Recruitment+=1
            elif str(i.process)=='Training':
                Training+=1
            elif str(i.process)=='Management':
                Management+=1
            elif str(i.process)=='Procurement':
                Procurement+=1
            elif str(i.process)=='Projects':
                Projects+=1
            elif str(i.process)=='Technical Support':
                TechnicalSupport+=1
            elif str(i.process) =='Customer Satisfaction':
                CustomerSatisfaction+=1
            elif str(i.process)=='Marketing':
                Marketing+=1
            elif str(i.process)=='Administration':
                Administration+=1
            else:
                pass
    ca_categories=['BidManagement','ITOperations','InternalAuditing','AccountsReceivables','AccountsPayables','Recruitment','Training','Management','Procurement','Projects','TechnicalSupport','CustomerSatisfaction','Marketing','Administration']
            
    nonconformities = {
        'name': 'NonConformity',
        'data':[BidManagement,IToperations,InternalAuditing,AccountsReceivables,AccountsPayables,Recruitment,Training,Management,Procurement,Projects,TechnicalSupport,CustomerSatisfaction,Marketing,Administration],
        'color': ''
    }

    ca_chart = {
        'chart': {'type': 'column'},
        'title': {'text': ' Process Non-Conformities'},
        'credits': 'false',
       
        'xAxis': {'categories': ca_categories},
        'series': [nonconformities],
           
    }
    ca_dump = json.dumps(ca_chart)

    
    #total_tasks_pending=total_ServiceRequests_pending  + total_RISKS_pending + total_OPPORTUNITY_pending + total_QMSplanner_pending + total_Trainingplanner_pending + total_INCIDENTREGISTER_pending + total_CORRECTIVEACTION_pending  + total_CUSTOMERSATISFACTION_pending + total_CUSTOMERCOMPLAINT_pending + total_PROVIDERASSESSMENT_pending
    context={'Executive_Tasks':ExecutiveTasks,'AnalystTopManager_Tasks':AnalystTopManager_Tasks,'AnalystAuditor_Tasks':AnalystAuditor_Tasks,'TopManagerAuditor_Tasks':TopManagerAuditor_Tasks,'AnalystTopManagerAuditor_Tasks':AnalystTopManagerAuditor_Tasks,'Analyst_Tasks':Analyst_Tasks,'Auditor_Tasks':Auditor_Tasks,'TopManager_Tasks':TopManager_Tasks,'ca_dump':ca_dump,'BidManagement':BidManagement,'ITOperations':IToperations,'InternalAuditing':InternalAuditing,'AccountsReceivables':AccountsReceivables,'AccountsPayables':AccountsPayables,'Recruitment':Recruitment,'Training':Training,'Management':Management,'Procurement':Procurement,'Projects':Projects,'TechnicalSupport':TechnicalSupport,'CustomerSatisfaction':CustomerSatisfaction,'Marketing':Marketing,'Administration':Administration,'finding':finding,'low':low,'high':high,'medium':medium,'total_jobs_pending':total_jobs_pending,'total_jobs_created':total_jobs_created,'total_jobs_completed':total_jobs_completed,'first_cost':g,'second_cost':h,'third_cost':m,'forth_cost':j,'fifth_cost':k,'sixth_cost':l,'firstt':aa,'secondd':bb,'thirdd':cc,'forthh':dd,'fifthh':ee,'sixthh':ff,'first':a,'second':b,'third':c,'forth':d,'fifth':e,'sixth':f,'poor':w,'improvement':x,'satisfactory':y,'good':z,'excellent':s,'browser_stats':browser_stats,'total_PROVIDERASSESSMENT':total_PROVIDERASSESSMENT,'total_CUSTOMERCOMPLAINT':total_CUSTOMERCOMPLAINT,'total_CUSTOMERSATISFACTION':total_CUSTOMERSATISFACTION,'total_CHANGEREQUEST':total_CHANGEREQUEST,'total_CORRECTIVEACTION':total_CORRECTIVEACTION,'total_INCIDENTREGISTER':total_INCIDENTREGISTER,'total_Trainingplanner':total_Trainingplanner,'total_QMSplanner':total_QMSplanner,'carstatus':carstatus,'cars':cars, 'customers':customers,'total_cars':total_cars,'total_approved':total_approved,'total_pending':total_pending,'counts':counts,'due':due,'chart': dump,'charts': dump2,'total_tasks':total_tasks,'total_tasks_pending':total_tasks_pending,'total_tasks_rejected':total_tasks_rejected,'total_IPS':total_IPS,'total_ISSUES':total_ISSUES,'total_COMPLAINCE':total_COMPLAINCE,'total_RISKS':total_RISKS,'total_OPPORTUNITY':total_OPPORTUNITY,'total_ServiceRequests_rejected':total_ServiceRequests_rejected,'total_QMSplanner_rejected':total_QMSplanner_rejected,'total_Trainingplanner_rejected':total_Trainingplanner_rejected,'total_INCIDENTREGISTER_rejected':total_INCIDENTREGISTER_rejected,'total_CORRECTIVEACTION_rejected':total_CORRECTIVEACTION_rejected,'total_CUSTOMERSATISFACTION_rejected':total_CUSTOMERSATISFACTION_rejected,'total_CUSTOMERCOMPLAINT_rejected':total_CUSTOMERCOMPLAINT_rejected,'total_PROVIDERASSESSMENT_rejected':total_PROVIDERASSESSMENT_rejected,'total_ServiceRequests_pending':total_ServiceRequests_pending,'total_RISKS_pending':total_RISKS_pending,'total_OPPORTUNITY_pending':total_OPPORTUNITY_pending,'total_QMSplanner_pending':total_QMSplanner_pending,'total_Trainingplanner_pending':total_Trainingplanner_pending,'total_INCIDENTREGISTER_pending':total_INCIDENTREGISTER_pending,'total_CORRECTIVEACTION_pending':total_CORRECTIVEACTION_pending,'total_CUSTOMERSATISFACTION_pending':total_CUSTOMERSATISFACTION_pending,'total_CUSTOMERCOMPLAINT_pending':total_CUSTOMERCOMPLAINT_pending,'total_PROVIDERASSESSMENT_pending':total_PROVIDERASSESSMENT_pending,'total_IPS_rejected':total_IPS_rejected,'total_ISSUES_rejected':total_ISSUES_rejected,'total_CHANGEREQUEST_rejected':total_CHANGEREQUEST_rejected,'total_ServiceRequests':total_ServiceRequests,'total_COMPLAINCE_rejected':total_COMPLAINCE_rejected,'tasks':tasks,'total_TRAININGevaluation':total_TRAININGevaluation,'total_TRAININGevaluation_pending':total_TRAININGevaluation_pending,'total_TRAININGevaluation_rejected':total_TRAININGevaluation_rejected,'total_CORRECTIVEACTION_pending_planning':total_CORRECTIVEACTION_pending_planning

}


 

    return render(request,'accounts/dashboard.html',context)






############# MSEM                   ##########################################
########FUNCTION TO FETCH CAR NON CONFORMITY LIST FROM NonConformityList TABLE BASED ON THE SOURCE SELECTED BY USER####

@login_required(login_url='login')
def car_approval(request):
    car_approval=car.objects.all()
    return render(request,'accounts/car_approve_form.html',{'car_approval':car_approval})


def CARerror(request):
    #print("PRINTING MESSAGES",messages)
    return render(request,'accounts/errors.html')

@login_required(login_url='login')
def createCARs(request):
        form=CARs()
        today=date.today()
        request.POST=request.POST.copy()
        request.POST['entered_by'] = request.user
        request.POST['car_date']=today
        request.POST['status'] = 5 #flaging status as pending car
                
        if request.method=="POST":
            form=CARs(request.POST)
                        
            if form.is_valid():
                form.added_by = request.user

                form.save()
                return redirect('/')
            
            
            form=CARs(request.POST)
            context={'form':form}
            print("PRINTING CONTEXT",context)
            return render(request,'accounts/car_form_new Copy.html',context)
           
        
        context={'form':form,'today':today}
        return render(request,'accounts/car_form_new Copy.html',context)


@login_required(login_url='login')
def createCAR(request):
        form=CARForm()
        forms=CARForm()
        if request.method=="POST":
            #print('Printing order:', request.POST)
            form=CARForm(request.POST)
            if form.is_valid():
                
                context={'car_number':request.POST.get('car_number'),
                'car_dateoccur':request.POST.get('car_dateoccur'),'car_time':request.POST.get('car_time'),
                'car_dept':request.POST.get('car_dept'),'car_userid':request.POST.get('car_userid'),
                'nonconf':request.POST.get('nonconf')}

                data=NonConformityList.objects.filter(source_id=request.POST.get('nonconf'))
 
                nonConformityAction=NonConformityAction.objects.all()
                rootCause=RootCause.objects.all()
                correctivePreventiveAction=CorrectivePreventiveAction.objects.all()
                priority=CarPriority.objects.all()
                all_users= get_user_model().objects.all()
                return render(request, 'accounts/car_form details.html',{'data':data,'context':context,
                'nonConformityAction':nonConformityAction,'rootCause':rootCause,'correctivePreventiveAction':correctivePreventiveAction,'priority':priority,
                'all_users':all_users})
                

                
        
        context={'form':form}
        return render(request,'accounts/car_form.html',context)

########FUNCTION TO SAVE CAR DETAILS TO CAR DATABASE#####################
@login_required(login_url='login')
def SaveCAR(request):
    form=CARFormSave()
    if request.method=="POST":
        request.POST=request.POST.copy()
        
        request.POST['entered_by'] = request.user
        #print("PRINTING request.POST['entered_by']",request.POST['entered_by'])
        form=CARFormSave(request.POST)
        #Set CAR status to pending before saving
        
        form.added_by = request.user

        
        print("PRINTING USER",form.added_by)
        
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            messages.info(request,'Forms has errors' )

    context={'form':form}
    
    #return render(request,'accounts/car_form details.html',context)
    return render(request,'accounts/errors.html',)
        



def product(request):
    products=Product.objects.all()
    return render(request,'accounts/product.html',{'products':products})

@login_required(login_url='login')
def cars_view(request):
    #car_list=car.objects.all()
    #car_list={'Car':Car}
    

    products=car.objects.all()
    myFilter=CarFilter(request.GET, queryset=products)
    products=myFilter.qs

    #print("printing method",request.method)

    #print("printing filter list",products)

    if request.method=="POST":
        car_list = car.objects.all()
        myFilter=CarFilter(request.GET, queryset=car_list)
        cars=myFilter.qs
        #print("PRINTING",cars)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="CAR.csv"'

        writer = csv.writer(response)
        writer.writerow(['CAR Number', 'CAR Date', 'CAR Dept', 'Reported by', 'Non Conformity','Description','Action Taken','Other Action','Root  cause','Other Root cause','Corrective Action','Other Corrective action',
'Proposed by','Proposed Date','Deadline', 'Priority','Implemented by','Entry Date','Entered by','Car status','Verification status'])

    
        for i in cars:
            
            writer.writerow([i.car_number, i.car_dateoccur, i.car_dept, i.car_userid,i.nonconf,i.description,i.action,i.CAother,i.rootcause,i.Rootother,i.correctiveaction,i.correctiveactionOther,
i.proposedby,i.proposedDate,i.deadline, i.priority,i.implementedby,i.car_date,i.entered_by,i.status,i.verification])
        return response
        
    else:
        #print("PRINTING",products)
        return render(request,'accounts/car_view.html',{'products':products,'myFilter':myFilter})




@login_required(login_url='login')
def cars_7daysToExpiryview(request,pk_test):

    products=car.objects.filter(car_number=pk_test)
    return render(request,'accounts/car_view_7_days_To_expiry.html',{'products':products})

def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all() #get all customer orders
	order_count = orders.count() #get total orders for the custoemr

	context = {'customer':customer, 'orders':orders, 'order_count':order_count}
	return render(request, 'accounts/customer.html',context)


def createorder(request):
        form=OrderForm()
        if request.method=="POST":
            #print('Printing order:', request.POST)
            form=OrderForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')
        context={'form':form}
        return render(request,'accounts/order_form.html',context)

def updateorder(request,pk_test):
    order=Order.objects.get(id=pk_test)
    form=OrderForm(instance=order)

    if request.method=="POST":
            #print('Printing order:', request.POST)
            form=OrderForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                return redirect('/')

    context={'form':form}  


    return render(request,'accounts/order_form.html',context)


@login_required(login_url='login')
def edit_car(request,pk_test):
    editcar=mod9001_risks.objects.get(risk_number=pk_test)
    form=CAReditForm(instance=editcar)

    if request.method=="POST":
            #print('Printing order:', request.POST)
            form=CAReditForm(request.POST, instance=editcar)
            if form.is_valid():
                form.save()
                return redirect('/')

    context={'form':form}  


    return render(request,'accounts/car_form_new copy.html',context)

@login_required(login_url='login')
def car_approve(request):
    approvecar=car.objects.filter(status="Pending")
    #if request.method=="POST":
       # approvecar.save()
       # return redirect('/')

    context={'item':approvecar}
  
    return render(request,'accounts/car_approve.html',context)

def deleteorder(request,pk_test):
    order=Order.objects.get(id=pk_test)
    if request.method=="POST":
        order.delete()
        return redirect('/')

    context={'item':order}
  
    return render(request,'accounts/delete.html',context)

@login_required(login_url='login')
def deletecar(request,pk_test):
    deletecar=car.objects.get(car_number=pk_test)
    if request.method=="POST":
        deletecar.delete()
        return redirect('/')

    context={'item':deletecar}
  
    return render(request,'accounts/delete.html',context)


#@login_required(login_url='login')
@unauthenticated_user
def register(request):
    
    form=CreateUser()
    if request.method=="POST":
        form=CreateUser(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,'Action Successful for user : '+username)
            return render(request,'accounts/login.html')
        

    context={'form':form}

    return render(request,'accounts/register.html',context)

@unauthenticated_user
def loginpage(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
           
            


            return redirect('home')
        else:
            messages.info(request,'Username or password incorrect')
            context={}
            return render(request,'accounts/login.html',context)

    context={}

    return render(request,'accounts/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def cars_pending(request):
    pendingcar=car.objects.filter(status='5') #get all cars pending approval    
    context={'pendingcar':pendingcar} 
    return render(request,'accounts/car_pending.html',context)

def CARnumbers_7days_expire(*x):
    date_str = x[0]
    date_object = datetime.strptime(date_str, '%m/%d/%Y').date()
    delta =date_object - date.today()
    return delta.days


@login_required(login_url='login')
def cars_7daystoEpirepending(request):
    carExpire7days=car.objects.filter(status=4).filter(~Q(verification=1))
    thislist = []
    for i in carExpire7days:
        w=i.deadline
        t=w.strftime('%m/%d/%Y')
        if CARnumbers_7days_expire(t)<8 and CARnumbers_7days_expire(t)>=0 :
            thislist.append(i.car_number)
    thisdict={}
    i=0
    #creat a dictionary for all car numbers for display
    for x in thislist:
        while i<len(thislist):
            y = str(i)
            thisdict["car_number"+y] = thislist[i]
            i+=1

        
    return render(request,'accounts/car_expire_in_ 7_days.html',{'thisdict':thisdict})



@login_required(login_url='login')
def cars_due(request):
    carExpire7days=car.objects.filter(status=4).filter(~Q(verification=1))
    thislist = []
    for i in carExpire7days:
        w=i.deadline
        t=w.strftime('%m/%d/%Y')
        if CARnumbers_7days_expire(t)<0:
            thislist.append(i.car_number)
    thisdict={}
    i=0
    #creat a dictionary for all car numbers for display
    for x in thislist:
        while i<len(thislist):
            y = str(i)
            thisdict["car_number"+y] = thislist[i]
            i+=1

        
    return render(request,'accounts/car_due.html',{'thisdict':thisdict})




@login_required(login_url='login')
def car_editing(request):
    
    all_car=car.objects.all() #get all cars in database 
   
    
    context={'all_car':all_car} 

    return render(request,'accounts/car editing.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['supervisor'])
def approve_car(request,pk_test):
    pending_car=car.objects.get(car_number=pk_test)
    form=ApproveCar(instance=pending_car)

    if request.method=="POST":
            #print('Printing order:', request.POST)
            form=ApproveCar(request.POST, instance=pending_car)
            if form.is_valid():
                form.save()
                return redirect('/cars_pending/')

    context={'form':form}  


    return render(request,'accounts/car_approve.html',context)

@allowed_users(allowed_roles=['supervisor'])
def verify_car(request,pk_test):
    open_car=car.objects.get(car_number=pk_test)
    form=VerifyCar(instance=open_car)
    if request.method=="POST":
            print('Printing REJECTED:', request.POST['verification_status'])
            if request.POST['verification_status'] =="Rejected":
                request.POST=request.POST.copy()
                request.POST['status'] = 5
            form=VerifyCar(request.POST, instance=open_car)
            if form.is_valid():
                form.save()
                return redirect('/cars_due/')

    context={'form':form}  


    return render(request,'accounts/car_verify.html',context)




def hideshow(request):
    return render(request,'accounts/date_validation.html')

#############HICHARTS VIEW######################

def ticket_class_view_3(request):
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
        .order_by('ticket_class')

    categories = list()
    survived_series_data = list()
    not_survived_series_data = list()

    for entry in dataset:
        categories.append('%s Class' % entry['ticket_class'])
        survived_series_data.append(entry['survived_count'])
        not_survived_series_data.append(entry['not_survived_count'])

    survived_series = {
        'name': 'Survived',
        'data': survived_series_data,
        'color': 'green'
    }

    not_survived_series = {
        'name': 'Survived',
        'data': not_survived_series_data,
        'color': 'red'
    }

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Titanic Survivors by Ticket Class'},
        'xAxis': {'categories': categories},
        'series': [survived_series, not_survived_series]
    }

    dump = json.dumps(chart)

    return render(request, 'accounts/ticket_class_2.html', {'chart': dump})


@login_required(login_url='login')
def user_profile(request):
    my_profile=employees.objects.filter(system_user_id=request.user.id)
    group=None
    
    if request.user.groups.exists():
        group=request.user.groups.all()
    
    context={'my_profile':my_profile,'group':group,'user':request.user}
    return render(request,"accounts/UserProfile.html",context)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_profile')
        #else:
            #messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })






