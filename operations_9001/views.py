from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from. forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth import get_user_model
from .decorators import unauthenticated_user,allowed_users

from django.contrib.auth.decorators import login_required
from datetime import date
import json
from django.db.models import Count, Q, F
import xlwt
from django.contrib.auth.models import User
from xlutils.copy import copy # http://pypi.python.org/pypi/xlutils
from xlrd import open_workbook # http://pypi.python.org/pypi/xlrd
import os
import csv
from .filters import *

# Create your views here.

##FUNCTIONS TO GENERATE IDs###########

def QMS_no():
   return str("Comp-QP-"+(date.today()).strftime("%d%m%Y"))+str(randint(0, 999))


def Train_no():
   return str("Comp-TR-Q-"+(date.today()).strftime("%d%m%Y"))+str(randint(0, 999))

def plan_no():
   return str("Comp-TP-Q-"+(date.today()).strftime("%d%m%Y"))+str(randint(0, 999))

def incident_no():
   return str("Comp-INC-IS-"+(date.today()).strftime("%d%m%Y"))+str(randint(0, 999))


def customer_no():
   return str("CST-MM-"+(date.today()).strftime("%d%m%Y"))+str(randint(0, 999))

def emp_perfrev_no():
   return str("Comp-EA-Q-"+(date.today()).strftime("%d%m%Y"))+str(randint(0, 999))



####################################################################################
def dateValidation(request):
    return render(request,'validation.html')


@login_required(login_url='login')
def maintenance(request):
              
    form=mentainance()
                          
    if request.method=="POST":

        request.POST=request.POST.copy()
        request.POST['entered_by'] = request.user
        request.POST['date_today']=date.today()
        
        form=mentainance(request.POST)
                        
        if form.is_valid():

                
            form.save()
            return redirect('/')
            
            
          
        
    context={'form':form}
    return render(request,'maintenance.html',context)






@login_required(login_url='login')
def cali(request):
              
    form=calibration()
                          
    if request.method=="POST":

        request.POST=request.POST.copy()
        request.POST['entered_by'] = request.user
        request.POST['date_today']=date.today()
        
        form=calibration(request.POST)
                        
        if form.is_valid():

                
            form.save()
            return redirect('/')
        
            
          
        
    context={'form':form}
    return render(request,'calibration.html',context)




@login_required(login_url='login')
def doc_manager(request):

    form=document_manager()
    

    
    if request.method=="POST":

        request.POST=request.POST.copy()
        request.POST['entered_by'] = request.user
        request.POST['date_today']=date.today()
        
           
        form = document_manager(request.POST)
        print("doc manager",request.POST)
        
         
            
        
        if form.is_valid():
           
            
            form.save()
           
            return redirect('/')
            
            
        form=document_manager(request.POST)
        context={'form':form}
        
        return render(request,'document_manager.html',context)
           
        
    context={'form':form}
    return render(request,'document_manager.html',context)



@login_required(login_url='login')
def qms_planner(request):
              
    form=qmsplanner(initial={'planner_number': QMS_no()})
                          
    if request.method=="POST":

        request.POST=request.POST.copy()
        request.POST['entered_by'] = request.user
        request.POST['date_today']=date.today()
        request.POST['status'] = 5
        
        form=qmsplanner(request.POST)
                        
        if form.is_valid():

                
            form.save()
            form=qmsplanner(initial={'planner_number': QMS_no()})
            context={'form':form}
            return render(request,'qmsplanner.html',context)
            #return redirect('/')
            
            
          
        
    context={'form':form}
    return render(request,'qmsplanner.html',context)

@login_required(login_url='login')
def qms_report(request):
    
    qms=mod9001_qmsplanner.objects.all() #get all qms planner in database 
    myFilter=planning_qmsFilter(request.GET, queryset=qms)
    qms=myFilter.qs
    if request.method=="POST":
        qms_list = mod9001_qmsplanner.objects.all()
        myFilter=planning_qmsFilter(request.GET, queryset=qms_list)
        qms=myFilter.qs
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="QMS_planner.csv"'

        writer = csv.writer(response)
        writer.writerow(['Planner No.', 'Plan Date', 'ProgramDescription', 'AdditionalDescription','Planner','StartDate','EndDate','Approval','Verification'])

    
        for i in qms:
            
            writer.writerow([i.planner_number, i.plan_date,i.description,  i.details,i.planner,i.start,i.end,i.status,i.qmsstatus])
        return response
        
    else:
        return render(request,'qms_report.html',{'qms':qms,'myFilter':myFilter})


@login_required(login_url='login')
def qms_pending(request):
    pendingcar=mod9001_qmsplanner.objects.filter(status='5') #get all qms pending approval    
    context={'pendingcar':pendingcar} 
    return render(request,'qms_pending.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['supervisor'])
def approve_qms(request,pk_test):
    pending_risk=mod9001_qmsplanner.objects.get(planner_number=pk_test)
    form=ApproveQMS(instance=pending_risk)

    if request.method=="POST":

            
            
            request.POST=request.POST.copy()
            request.POST['approved_by']=request.user
            request.POST['approval_date']=date.today()                      

            form=ApproveQMS(request.POST, instance=pending_risk)
            if form.is_valid():
                form.save()
                return redirect('/qms_pending/')

    context={'form':form}  


    return render(request,'qms_approve.html',context)



#####################################QMS VERIFICATION##############################
@login_required(login_url='login')
def opp_7daysToExpiryview(request,pk_test):

    products=mod9001_qmsplanner.objects.filter(planner_number=pk_test)
    return render(request,'qms_view_7_days_To_expiry.html',{'products':products})




def CARnumbers_7days_expire(*x):
    date_str = x[0]
    date_object = datetime.strptime(date_str, '%m/%d/%Y').date()
    delta =date_object - date.today()
    return delta.days


@login_required(login_url='login')
def qms_due(request):
    carExpire7days=mod9001_qmsplanner.objects.filter(status=1).filter(~Q(qmsstatus=1))
    thislist = []
    for i in carExpire7days:
        w=i.end
        t=w.strftime('%m/%d/%Y')
        if CARnumbers_7days_expire(t)<0:
            thislist.append(i.planner_number)
    thisdict={}
    i=0
    #creat a dictionary for all car numbers for display
    for x in thislist:
        while i<len(thislist):
            y = str(i)
            thisdict["planner_number"+y] = thislist[i]
            i+=1

        
    return render(request,'qms_due.html',{'thisdict':thisdict})



@login_required(login_url='login')
def qms_7daysToExpiryview(request,pk_test):

    products=mod9001_qmsplanner.objects.filter(planner_number=pk_test)
    return render(request,'qms_view_7_days_To_expiry.html',{'products':products})

@allowed_users(allowed_roles=['supervisor'])
def verify_qms(request,pk_test):
    open_car=mod9001_qmsplanner.objects.get(planner_number=pk_test)
    form=VerifyQMS(instance=open_car)
    if request.method=="POST":
            print("request.POST['qmsstatus']",request.POST['qmsstatus'])
            
            if request.POST['qmsstatus'] =="Rejected":
                request.POST=request.POST.copy()
                request.POST['status'] = 5 #requires approval first before next verification
                request.POST['verification']=2 #default verifiaction to Not effective
                print("request", request.POST)
            
            elif request.POST['qmsstatus'] == '1':
                print("request.POST['qmsstatus']",request.POST['qmsstatus'])
                request.POST=request.POST.copy()
                request.POST['status'] = 1 # keep status approved
            
            else:
                request.POST=request.POST.copy()






            form=VerifyQMS(request.POST, instance=open_car)
            if form.is_valid():
                form.save()
                return redirect('/qms_due/')

    context={'form':form}  


    return render(request,'qms_verify.html',context)



#######################TRAINING REGISTER###############################
@login_required(login_url='login')
def training_register(request):
              
    form=trainingregister(initial={'training_number': Train_no()})
                          
    if request.method=="POST":

        request.POST=request.POST.copy()
        request.POST['entered_by'] = request.user
        request.POST['date_today']=date.today()
        
        form=trainingregister(request.POST)
                        
        if form.is_valid():

                
            form.save()
            form=trainingregister(initial={'training_number': Train_no()})
            context={'form':form}
            return render(request,'trainingregister.html',context)
            #return redirect('/')
            
            
          
        
    context={'form':form}
    return render(request,'trainingregister.html',context)


#######################TRAINING PLANNER ###############################
@login_required(login_url='login')
def training_planner(request):
              
    form=trainingplaner(initial={'plan_number': plan_no()})
                          
    if request.method=="POST":

        request.POST=request.POST.copy()
        request.POST['entered_by'] = request.user
        request.POST['date_today']=date.today()
        request.POST['status'] = 5
        
        form=trainingplaner(request.POST)
                        
        if form.is_valid():

                
            form.save()
            form=trainingplaner(initial={'plan_number': plan_no()})
            context={'form':form}
            return render(request,'trainingplanner.html',context)
            #return redirect('/')
            
            
          
        
    context={'form':form}
    return render(request,'trainingplanner.html',context)

@login_required(login_url='login')
def trainingplan_report(request):
    
    trainingplan=mod9001_trainingplanner.objects.all() #get all qms planner in database 
    myFilter=planning_trainingplannerFilter(request.GET, queryset=trainingplan)
    trainingplan=myFilter.qs
    if request.method=="POST":
        trainingplan_list = mod9001_trainingplanner.objects.all()
        myFilter=planning_trainingplannerFilter(request.GET, queryset=trainingplan_list)
        trainingplan=myFilter.qs
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Training_planner.csv"'

        writer = csv.writer(response)
        writer.writerow(['Planner No.', 'TrainingType', 'Description', 'AdditionalDescription','Date','Audience','Objective','StartDate','EndDate','Location','Trainer','Resources','Approval','Verification'])

    
        for i in trainingplan:
            
            writer.writerow([i.plan_number, i.get_type_display(),i.description,  i.details,i.trainng_date,i.get_trainaudience_display(),i.objective,i.start,i.end,i.get_trainlocation_display(),i.trainer,i.status,i.trainplannerstatus])
        return response
        
    else:
        return render(request,'trainingplan_report.html',{'trainingplan':trainingplan,'myFilter':myFilter})



@login_required(login_url='login')
def trainplanner_pending(request):
    pendingcar=mod9001_trainingplanner.objects.filter(status='5') #get all  pending approval    
    context={'pendingcar':pendingcar} 
    return render(request,'trainplanner_pending.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['supervisor'])
def approve_trainplanner(request,pk_test):
    pending_risk=mod9001_trainingplanner.objects.get(plan_number=pk_test)
    form=ApproveTrainingPlanner(instance=pending_risk)

    if request.method=="POST":

            
            
            request.POST=request.POST.copy()
            request.POST['approved_by']=request.user
            request.POST['approval_date']=date.today()                      

            form=ApproveTrainingPlanner(request.POST, instance=pending_risk)
            if form.is_valid():
                form.save()
                return redirect('/trainplanner_pending/')

    context={'form':form}  


    return render(request,'trainingplanner_approve.html',context)


#####################################TRAIN PLANNER VERIFICATION##############################




def CARnumbers_7days_expire(*x):
    date_str = x[0]
    date_object = datetime.strptime(date_str, '%m/%d/%Y').date()
    delta =date_object - date.today()
    return delta.days


@login_required(login_url='login')
def training_due(request):
    carExpire7days=mod9001_trainingplanner.objects.filter(status=1).filter(~Q(trainplannerstatus=1))
    thislist = []
    for i in carExpire7days:
        w=i.end
        t=w.strftime('%m/%d/%Y')
        if CARnumbers_7days_expire(t)<0:
            thislist.append(i.plan_number)
    thisdict={}
    i=0
    #creat a dictionary for all car numbers for display
    for x in thislist:
        while i<len(thislist):
            y = str(i)
            thisdict["plan_number"+y] = thislist[i]
            i+=1

        
    return render(request,'training_due.html',{'thisdict':thisdict})



@login_required(login_url='login')
def qms_7daysToExpiryview(request,pk_test):

    products=mod9001_qmsplanner.objects.filter(planner_number=pk_test)
    return render(request,'qms_view_7_days_To_expiry.html',{'products':products})

@allowed_users(allowed_roles=['supervisor'])
def verify_training(request,pk_test):
    open_car=mod9001_trainingplanner.objects.get(plan_number=pk_test)
    form=VerifyTraining(instance=open_car)
    if request.method=="POST":
            #print("request.POST['qmsstatus']",request.POST['qmsstatus'])
            
            if request.POST['trainplannerstatus'] =="Rejected":
                request.POST=request.POST.copy()
                request.POST['status'] = 5 #requires approval first before next verification
                request.POST['verification']=2 #default verifiaction to Not effective
                #print("request", request.POST)
            
            elif request.POST['trainplannerstatus'] == '1':
                #print("request.POST['qmsstatus']",request.POST['qmsstatus'])
                request.POST=request.POST.copy()
                request.POST['status'] = 1 # keep status approved
            
            else:
                request.POST=request.POST.copy()






            form=VerifyTraining(request.POST, instance=open_car)
            if form.is_valid():
                form.save()
                return redirect('/training_due/')

    context={'form':form}  


    return render(request,'training_verify.html',context)


@login_required(login_url='login')
def training_7daysToExpiryview(request,pk_test):

    products=mod9001_trainingplanner.objects.filter(plan_number=pk_test)
    return render(request,'training_view_7_days_To_expiry.html',{'products':products})


@login_required(login_url='login')
def incidentRegister(request):
              
    form=incident_Register(initial={'incident_number': incident_no()})
                          
    if request.method=="POST":

        request.POST=request.POST.copy()
        request.POST['entered_by'] = request.user
        request.POST['date_today']=date.today()
        #request.POST['status'] = 5
        
        form=incident_Register(request.POST)
                        
        if form.is_valid():

                
            form.save()
            form=incident_Register(initial={'incident_number': incident_no()})
            context={'form':form}
            return render(request,'incidentRegister.html',context)
            
            
          
        
    context={'form':form}
    return render(request,'incidentRegister.html',context)
@login_required(login_url='login')
def incident_report(request):

    
    incident=mod9001_incidentregisterStaff.objects.all() #get all incident registers by staff
  
    
    
    myFilter=Operations_incidentRegisterFilter(request.GET, queryset=incident)
    incident=myFilter.qs
    if request.method=="POST":
        incident_list = mod9001_incidentregisterStaff.objects.all()
        
        myFilter=Operations_incidentRegisterFilter(request.GET, queryset=incident_list)
        incident=myFilter.qs
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="IncidentRegister.csv"'

        writer = csv.writer(response)
        writer.writerow(['Incident. No.', 'Date', 'Time', 'Reference','ProcessName','Type','Description','Details','Classification','RootCause','Containment','AsignedTo','DateAssigned','CompletionDate','CostDescription','LessonLearnt'])

    
        for i in incident:
            #if i.issue_number.get_context_display() is not None:#if the value is none django throws errors
            writer.writerow([i.incident_number, i.date,i.incident_number.time,i.incident_number.get_reference_display(),i.incident_number.processname,i.incident_number.incidentype,i.incident_number.incident_description,i.incident_number.other,i.classification,i.rootcause,i.get_correction_display(),i.assigned,i.date,i.completion,i.cost,i.lesson])
        return response
        
    else:
        return render(request,'incident_report.html',{'incident':incident,'myFilter':myFilter})









def load_description(request):
    context_id = request.GET.get('contextid')
    
    #ids = mod9001_risks.objects.filter(contextdetails_id=context_id)
    #ids = mod9001_issues.objects.all()
   
    #print("context_id incidents", context_id)
    ids=incident_description.objects.filter(incident_type_id=context_id)
    #or id in ids:
    #    print("ID  Description",id.incident_type_id,  id.description)

    
    return render(request, 'id_dropdown_list_option.html', {'ids': ids})


def load_process(request):
    context_id = request.GET.get('contextid')
    
    #ids = mod9001_risks.objects.filter(contextdetails_id=context_id)
    #ids = mod9001_issues.objects.all()
   
    print("context_id incidents", context_id)
    if context_id=="2":
        #print("ID  test",id.id,  id.description)
        ids=process.objects.all()
    else:
        ids=process.objects.filter(id=20)
    
    for id in ids:
        print("ID  Description",id.id,  id.description)

    
    return render(request, 'load_process_list.html', {'ids': ids})


@login_required(login_url='login')
def customerRegister(request):
              
    form=customer_Register(initial={'customer_number': customer_no()})
                          
    if request.method=="POST":

        request.POST=request.POST.copy()
        request.POST['entered_by'] = request.user
        request.POST['date_today']=date.today()
        #request.POST['status'] = 5
        
        form=customer_Register(request.POST)
                        
        if form.is_valid():

                
            form.save()
            form=customer_Register(initial={'customer_number': customer_no()})
            context={'form':form}
            return render(request,'customeRegister.html',context)
            
            
    context={'form':form}
    return render(request,'customeRegister.html',context)

@login_required(login_url='login')
def incidentRegisterStaff(request):
    form=incident_RegisterStaff()
              
                            
    if request.method=="POST":
        request.POST=request.POST.copy()
        request.POST['entered_by'] = request.user
        request.POST['date_today']=date.today()
        #request.POST['status'] = 5
        
        form=incident_RegisterStaff(request.POST)
                        
        if form.is_valid():

                
            form.save()
            form=incident_RegisterStaff()
            context={'form':form}
            return render(request,'incidentRegisterStaff.html',context)

            
            
          
        
    context={'form':form}
    return render(request,'incidentRegisterStaff.html',context)



@login_required(login_url='login')
def providerassessment(request):
    form=providerassessments(initial={'emp_perfrev_no': emp_perfrev_no()})
    providers=mod9001_supplieregistration.objects.values(organisation=F('name'))
    
              
                            
    if request.method=="POST":
        request.POST=request.POST.copy()
        request.POST['entered_by'] = request.user
        request.POST['date_today']=date.today()
        #request.POST['status'] = 5
        
        
        form=providerassessments(request.POST)
                        
        if form.is_valid():

                
            form.save()
            form=providerassessments()
            context={'form':form}
            return render(request,'providerassessment.html',context)

            
            
          
        
    context={'form':form,'providers':providers}
    return render(request,'providerassessment.html',context)



            
            
          
        



