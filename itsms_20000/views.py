from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from. forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth import get_user_model
#from .decorators import unauthenticated_user,allowed_users
from operations_9001.decorators import unauthenticated_user,allowed_users
from django.contrib.auth.decorators import login_required
from datetime import date,timedelta
import json
from django.db.models import Count, Q, F
import xlwt
from django.contrib.auth.models import User
from xlutils.copy import copy # http://pypi.python.org/pypi/xlutils
from xlrd import open_workbook # http://pypi.python.org/pypi/xlrd
import os
import csv
from .filters import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, Http404
from accounts.utils import *
from issues_9001.views import get_companyCode
from accounts.models import Customer
from django.utils.timesince import timeuntil

# Create your views here.
def duration(start, end):
    try:
        if start is not None and end is not None:
            return timeuntil(start,end)
        else:
            return ''
    except (ValueError, TypeError):
        return ''




def service_no():
   return str(get_companyCode()+"-SR-"+(date.today()).strftime("%d%m%Y"))+str(randint(0, 999))

def CARnumbers_7days_expire(*x):
    date_str = x[0]
    date_object = datetime.strptime(date_str, '%m/%d/%Y').date()
    delta =date_object - date.today()
    return delta.days


@login_required(login_url='login')
@allowed_users(allowed_roles=['Logger'])
def services_request(request):
              
    form=serviceRequest(initial={'service_number': service_no()})
                          
    if request.method=="POST":

        request.POST=request.POST.copy()

        request.POST['entered_by'] = request.user
        request.POST['date_today']=date.today()
        #request.POST['status'] = 5
        
        form=serviceRequest(request.POST)
                        
        if form.is_valid():

                
            form.save()
            form=serviceRequest(initial={'service_number': service_no()})
            context={'form':form}
            return render(request,'service_request.html',context)
            
            
          
        
    context={'form':form}
    return render(request,'service_request.html',context)


@login_required(login_url='login')
def service_request_report(request):

    
    service_request=mod20000_service_planning.objects.all() #get all service requests
  
    
    
    myFilter=serviceRequestFilter(request.GET, queryset=service_request)
    service_request=myFilter.qs
    if request.method=="POST":
        request_list = mod20000_service_planning.objects.all()
        
        myFilter=serviceRequestFilter(request.GET, queryset=request_list)
        service_request=myFilter.qs
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="ServiceRequests.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['SR ID', 'Date', 'Time', 'Type','Requestor','Mode','ITservice','Details','Priority','PlanningDate','Scope','Category','Resource','Dependency','PlanningDesc.','Activities','Criteria','AssignedTO','Completed','CompletedBy','ReportNo.','ComponentAffected','Error','Solution','Remark','Verification','Rescheduled','When','Duration'])
    
        for i in service_request:

                    
            writer.writerow([i.service_number, i.service_number.date,i.service_number.time,i.service_number.request_type,i.service_number.requestor,i.service_number.request_mode,i.service_number.IT_service,i.service_number.other,i.service_number.priority,i.planning_date,i.service_scope,i.service_category,i.get_resource_display(),i.get_dependency_display(),i.description,i.activities,i.get_criteria_display(),i.assigned,i.completion_date,i.completedby,i.report_number,i.component_affected,i.error,i.solution,i.remark,i.qmsstatus,i.scheduled,i.due,duration(i.completion_date,i.service_number.date)])
        return response
        
    else:
        return render(request,'serviceRequest_report.html',{'service_request':service_request,'myFilter':myFilter})

@login_required(login_url='login')
def serviceRequest_pending_planning(request):

    products=mod20000_service_request.objects.filter(planning_flag='No')
    return render(request,'serviceRequest_pending_planning.html',{'products':products})

@login_required(login_url='login')
def serviceRequest_rejected(request):

    products=mod20000_service_planning.objects.all().filter(date_today__gte=datetime.now() - timedelta(days=7)).filter(qmsstatus='3')
    return render(request,'serviceRequest_rejected.html',{'products':products})





@login_required(login_url='login')
@allowed_users(allowed_roles=['Analyst'])
def serviceRequestPlanning(request,sr_id):

    form=serviceRequestPlans(initial={'service_number':sr_id})
    #form=risk(initial={'risk_number': Risk_no(),'issue_number':issue_number})
              
                            
    if request.method=="POST":
        request.POST=request.POST.copy()
        request.POST['entered_by'] = request.user
        request.POST['date_today']=date.today()
        request.POST['status'] = 1
        #request.POST['status'] = 5
        
        form=serviceRequestPlans(request.POST)
                        
        if form.is_valid():
            #print("request.POST['qmsstatus']",request.POST)


                
            form.save()
            return redirect('/serviceRequest_pending_planning/')

            
            
          
        
    context={'form':form}
    return render(request,'serviceRequest_planning.html',context)


@login_required(login_url='login')
def serviceRequest_due(request):
    #carExpire7days=mod20000_service_planning.objects.filter(status=1).filter(~Q(qmsstatus=1))
    carExpire7days=mod20000_service_planning.objects.all().filter(due__gte=datetime.now() - timedelta(days=7)).filter(~Q(qmsstatus='3')).filter(~Q(qmsstatus='1'))
    #carExpire7days=mod9001_providerassessment.objects.filter(status=1)
    #thislist = []
    #for i in carExpire7days:
        #print("printing",i)
    #    if i.due is not None:
            #w=i.due
            #t=w.strftime('%m/%d/%Y')
            #if CARnumbers_7days_expire(t)<0:
    #        thislist.append(i.service_number)
    #thisdict={}
    #i=0
    #creat a dictionary for all car numbers for display
    #for x in thislist:
    #    while i<len(thislist):
    #        y = str(i)
     #       thisdict["service_number"+y] = thislist[i]
    #        i+=1

    context={'products':carExpire7days}    
    return render(request,'serviceRequest_due.html',context)




@login_required(login_url='login')
def serviceRequest_7daysToExpiryview(request,pk_test):

    products=mod20000_service_planning.objects.filter(service_number=pk_test)
    return render(request,'serviceRequest_view_7_days_To_expiry.html',{'products':products})

def Verify_service_request(request,pk_test):
    open_car=mod20000_service_planning.objects.get(service_number=pk_test)
    form=VerifyServiceRequest(instance=open_car)
   # print("request.POST['qmsstatus']",request.POST['qmsstatus'])
    if request.method=="POST":
            #print("request.POST['qmsstatus']",request.POST['qmsstatus'])
            
            if request.POST['qmsstatus'] =="3":
                request.POST=request.POST.copy()
                request.POST['status'] = '' #make it cancelled
                request.POST['verification_status']='' #make it canceled
                #request.POST['end']='1900-01-01'
                #print("#MAKE IT CANCELED",  request.POST['status'])
            
            elif request.POST['qmsstatus'] == '2':#if Not complete
                #print("request.POST['qmsstatus']",request.POST['qmsstatus'])
                request.POST=request.POST.copy()
                request.POST['status'] = 4 # keep status open
                #request.POST['verification_status']='Closed'
            elif request.POST['qmsstatus'] == '4':#if rescheduled
                #print("request.POST['qmsstatus']",request.POST['qmsstatus'])
                request.POST=request.POST.copy()
                request.POST['due'] = request.POST['scheduled'] # keep status open
                #print("RESCHEDULED",request.POST['end'])
            elif request.POST['qmsstatus'] == '1':
                request.POST=request.POST.copy()
                request.POST['status'] = 1 # keep status approved
                request.POST['verification_status']='Closed'
            else:
                request.POST=request.POST.copy()




            
            form=VerifyServiceRequest(request.POST, instance=open_car)
            #print("printing service_nmuber",open_car)
            #print("printing request.POST",request.POST)
            if form.is_valid():
                form.save()
                return redirect('/serviceRequest_due/')

    context={'form':form,'serviceRequest_id':pk_test}  


    return render(request,'serviceRequest_verify.html',context)