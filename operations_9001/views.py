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
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, Http404
from accounts.utils import *

# Create your views here.

##FUNCTIONS TO GENERATE IDs###########



def QMS_no():
   return str("TEGA-QP-"+(date.today()).strftime("%d%m%Y"))+str(randint(0, 999))


def Train_no():
   return str("TEGA-TR-Q-"+(date.today()).strftime("%d%m%Y"))+str(randint(0, 999))

def plan_no():
   return str("TEGA-TP-Q-"+(date.today()).strftime("%d%m%Y"))+str(randint(0, 999))

def incident_no():
   return str("TEGA-INC-IS-"+(date.today()).strftime("%d%m%Y"))+str(randint(0, 999))


def customer_no():
   return str("CST-MM-"+(date.today()).strftime("%d%m%Y"))+str(randint(0, 999))

def emp_perfrev_no():
   return str("TEGA-EA-Q-"+(date.today()).strftime("%d%m%Y"))+str(randint(0, 999))

def document_no():
   return str("TEGA-Q-"+(date.today()).strftime("%d%m%Y"))+str(randint(0, 999))

def comp_no():
   return str("TEGA-COMP-Q-"+(date.today()).strftime("%d%m%Y"))+str(randint(0, 999))

def satis_survey_no():
   return str("TEGA-CS-Q-"+(date.today()).strftime("%d%m%Y"))+str(randint(0, 999))


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
@allowed_users(allowed_roles=['DocumentController'])
def doc_manager(request):

    form=document_manager(initial={'document_number': document_no()})
    

    
    if request.method=="POST":

        request.POST=request.POST.copy()
        request.POST['entered_by'] = request.user
        request.POST['date_today']=date.today()
        
           
        form = document_manager(request.POST,request.FILES)
        #
        #print("doc manager",request.FILES)
        
         
            
        
        if form.is_valid():
           
            
            form.save()

                      
            return redirect('/')
            
            
        form=document_manager(request.POST)
        context={'form':form}
        
        return render(request,'document_manager.html',context)
           
        
    context={'form':form}
    return render(request,'document_manager.html',context)

@login_required(login_url='login')
def documentmanager_report(request):
    
    docmngr=mod9001_document_manager.objects.all() #get all qms planner in database 
    myFilter=documentmanagerFilter(request.GET, queryset=docmngr)
    docmngr=myFilter.qs
    if request.method=="POST":
        docmngr_list = mod9001_document_manager.objects.all()
        myFilter=documentmanagerFilter(request.GET, queryset=docmngr_list)
        docmngr=myFilter.qs
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Document_register.csv"'

        writer = csv.writer(response)
        writer.writerow(['DocumentNo.', 'ReferenceNo', 'Name', 'Type','Version','Format','Origin','Standard','StdClause','Location','Owner','Rentention','Status'])

    
        for i in docmngr:
            
            writer.writerow([i.document_number, i.document_id,i.doc_name,  i.doc_type,i.version,i.format,i.origin,i.standard,i.clause,i.location,i.owner,i.retention,i.status])
        return response
        
    else:
        return render(request,'documentmanager_report.html',{'docmngr':docmngr,'myFilter':myFilter})

def download(request, id):
    obj = your_model_name.objects.get(id=id)
    filename = obj.model_attribute_name.path
    response = FileResponse(open(filename, 'rb'))
    return response



@login_required(login_url='login')
@allowed_users(allowed_roles=['ManagementRepresentative'])
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
    if is_Auditor(request.user):
        pendingcar=mod9001_qmsplanner.objects.all().filter(status='5').filter(~Q(verification_status='Closed')) #get all qms pending approval    
        
    else:
        pendingcar=mod9001_qmsplanner.objects.filter(status='5') #get all qms pending approval
    
    context={'pendingcar':pendingcar} 
    return render(request,'qms_pending.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['TopManager'])
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

@allowed_users(allowed_roles=['Auditor'])
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
                request.POST['verification_status']='Closed'
            
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
@allowed_users(allowed_roles=['HRManager'])
def trainingReg(request):
    #print("PRINTING PRINTING")        
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

@login_required(login_url='login')
def training_register_report(request):
    
    trainingreg=mod9001_trainingregister.objects.all() #get all training register in the database 
    myFilter=trainingRegFilter(request.GET, queryset=trainingreg)
    trainingreg=myFilter.qs
    if request.method=="POST":
        trainingreg_list = mod9001_trainingregister.objects.all()
        myFilter=trainingRegFilter(request.GET, queryset=trainingreg_list)
        trainingreg=myFilter.qs
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Training_Evaluation_Report.csv"'

        writer = csv.writer(response)
        writer.writerow(['TainingNo','TrainingDescription.', 'AdditionalDescription', 'TrainingDate', 'Nature','Trainee','Dept','CompletionDate','Decision','Reason','Details','ActionPlan','AdditionalDesc.','AssignedTo','Timeline'])

    
        for i in trainingreg:
            
            writer.writerow([i.training_number, i.plan_number.description,i.plan_number.details, i.train_date,i.get_nature_display(),i.trainee,i.trainee.dept,i.completion_date,i.get_decision_display(),i.reasond,i.reasonother,i.actionplan,i.actionplanother,i.assigned,i.timeline])
        return response
        
    else:
        return render(request,'Training_Evaluation_Report.html',{'trainingreg':trainingreg,'myFilter':myFilter})
###################### TRAINING REGISTER VERIFICATION ############################################################


####################### TRAINING PLANNER ###############################
@login_required(login_url='login')
@allowed_users(allowed_roles=['HRManager'])
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
@allowed_users(allowed_roles=['TopManager'])
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


#####################################TRAINING PLANNER VERIFICATION##############################

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

@allowed_users(allowed_roles=['Auditor'])
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
                request.POST['verification_status']='Closed'
            
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

########################INCIDENT REGISTER################################################
@login_required(login_url='login')
@allowed_users(allowed_roles=['IncidentManager'])
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
        writer.writerow(['Incident. No.', 'Date', 'Time', 'Process','Type','Description','Details','Classification','Containment','Addit.Desc','AssignedTo','When','Comp.Date','Cost','currency','Amount','Lesson'])
    
        for i in incident:
            #if i.issue_number.get_context_display() is not None:#if the value is none django throws errors
            writer.writerow([i.incident_number, i.incident_number.date,i.incident_number.time,i.incident_number.processname,i.incident_number.incidentype,i.incident_number.incident_description,i.incident_number.other,i.classification,i.correction,i.description,i.assigned,i.due,i.completion,i.get_cost_display(),i.get_currency_display(),i.costdescription,i.lesson])
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
@allowed_users(allowed_roles=['ManagementRepresentative'])
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
@allowed_users(allowed_roles=['IncidentManager'])
def incidentRegisterStaff(request):

    form=incident_RegisterStaff()
              
                            
    if request.method=="POST":
        request.POST=request.POST.copy()
        request.POST['entered_by'] = request.user
        request.POST['date_today']=date.today()
        request.POST['status'] = 1
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
def incidentregister_due(request):
    carExpire7days=mod9001_incidentregisterStaff.objects.filter(status=1).filter(~Q(qmsstatus=1))
    #carExpire7days=mod9001_providerassessment.objects.filter(status=1)
    thislist = []
    for i in carExpire7days:
        #print("printing",i)
        w=i.due
        t=w.strftime('%m/%d/%Y')
        if CARnumbers_7days_expire(t)<0:
            thislist.append(i.incident_number)
    thisdict={}
    i=0
    #creat a dictionary for all car numbers for display
    for x in thislist:
        while i<len(thislist):
            y = str(i)
            thisdict["incident_number"+y] = thislist[i]
            i+=1

        
    return render(request,'incidentregister_due.html',{'thisdict':thisdict})





@allowed_users(allowed_roles=['Auditor'])
def Verify_incidentregister(request,pk_test):
    open_car=mod9001_incidentregisterStaff.objects.get(incident_number=pk_test)
    form=Verifyincidentregister(instance=open_car)
    if request.method=="POST":
            #print("request.POST['qmsstatus']",request.POST['qmsstatus'])
            
            if request.POST['qmsstatus'] =="Rejected":
                request.POST=request.POST.copy()
                request.POST['status'] = 1 #requires approval first before next verification
                request.POST['verification']=2 #default verifiaction to Not effective
                print("request", request.POST)
            
            elif request.POST['qmsstatus'] == '1':
                #print("request.POST['qmsstatus']",request.POST['qmsstatus'])
                request.POST=request.POST.copy()
                request.POST['status'] = 1 # keep status approved
                request.POST['verification_status']='Closed'
            
            else:
                request.POST=request.POST.copy()






            form=Verifyincidentregister(request.POST, instance=open_car)
            if form.is_valid():
                form.save()
                return redirect('/incidentregister_due/')

    context={'form':form}  


    return render(request,'incidentregister_verify.html',context)


@login_required(login_url='login')
def incidentregister_7daysToExpiryview(request,pk_test):

    products=mod9001_incidentregisterStaff.objects.filter(incident_number=pk_test)
    return render(request,'incidentregister_view_7_days_To_expiry.html',{'products':products})




@login_required(login_url='login')
@allowed_users(allowed_roles=['Assessor'])
def providerassessment(request):
    form=providerassessments(initial={'emp_perfrev_no': emp_perfrev_no()})
    providers=mod9001_supplieregistration.objects.values(organisation=F('name'))
    
              
                            
    if request.method=="POST":
        request.POST=request.POST.copy()
        request.POST['entered_by']=request.user
        request.POST['date_today']=date.today()
        request.POST['status'] = 1
#        #print("TEXT",request.POST)
        
        
        form=providerassessments(request.POST)
                        
        if form.is_valid():

                
            form.save()
            form=providerassessments()
            context={'form':form}
            return render(request,'providerassessment.html',context)

            
            
          
        
    context={'form':form,'providers':providers}
    return render(request,'providerassessment.html',context)

@login_required(login_url='login')
def providerAssessment_report(request):
    
    providerassessment=mod9001_providerassessment.objects.all() #get all qms planner in database 
    myFilter=providerAssessmentFilter(request.GET, queryset=providerassessment)
    providerassessment=myFilter.qs
    if request.method=="POST":
        providerassessment_list = mod9001_providerassessment.objects.all()
        myFilter=providerAssessmentFilter(request.GET, queryset=providerassessment_list)
        providerassessment=myFilter.qs
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="ProviderAssessment.csv"'

        writer = csv.writer(response)
       
        writer.writerow(['Review No.', 'Date', 'Provider', 'Organisation','Appraisee','Rating','ImprovementPlan','Addit.Details','AssignedTo','Timeline','Status'])

    
        for i in providerassessment:
            #def improvementPlan():
            #    if i.jobknowledg:
            #        return "Organisation:"
            #   else:
            #        return " "
            def jobknowledg():
                if i.jobknowledg:
                    return " Job Knowledge:"
                else:
                    return " "
            def flexibility():
                if i.flexibility:
                    return " ,Adaptability:"
                else:
                    return " "                         
            def problemsolving():
                if i.problemsolving:
                    return " ,Problem solving:"
                else:
                    return " "                    
            def Initiativenes():
                if i.Initiativenes:
                    return " ,Initiativenes:"
                else:
                    return " " 
            def planning():
                if i.planing:
                    return " ,Planning & Org.:"
                else:
                    return " "                            
            def workquality():
                if i.workquality:
                    return " ,Work Quality:"
                else:
                    return " " 
            def interskills():
                if i.interskills:
                    return " ,Interpersonal skills:"
                else:
                    return " " 
            def communication():
                if i.communication:
                    return " ,Communication skills:"
                else:
                    return " " 
            def supervisionmagt():
                if i.supervisionmagt:
                    return " ,Supervision & mngt:"
                else:
                    return " " 
            def availabilit():
                if i.availabilit:
                    return " ,Availability:"
                else:
                    return " " 
            def professional():
                if i.professional:
                    return " ,Professional contribution:"
                else:
                    return " " 
        
            writer.writerow([i.emp_perfrev_no, i.start,i.get_Provider_display(),i.organisation,i.appraise,i.rank,jobknowledg()+ i.get_jobknowledg_display() + flexibility()+ i.get_flexibility_display()+ problemsolving()+ i.get_problemsolving_display()+ Initiativenes()+ i.get_Initiativenes_display()+ planning()+ i.get_planing_display()+ workquality()+ i.get_workquality_display()+ interskills()+ i.get_interskills_display()+ communication()+ i.get_communication_display()+ supervisionmagt()+ i.get_supervisionmagt_display()+ availabilit()+ i.get_availabilit_display()+ professional()+ i.get_professional_display()
            ,i.nonconfdetails,i.assigned,i.due,i.qmsstatus])
            
        return response
        
    else:
        return render(request,'providerAssessment_report.html',{'providerassessment':providerassessment,'myFilter':myFilter})







@login_required(login_url='login')
def providerassessments_due(request):
    carExpire7days=mod9001_providerassessment.objects.filter(status=1).filter(~Q(qmsstatus=1))
    #carExpire7days=mod9001_providerassessment.objects.filter(status=1)
    thislist = []
    for i in carExpire7days:
        #print("printing",i)
        w=i.due
        t=w.strftime('%m/%d/%Y')
        if CARnumbers_7days_expire(t)<0:
            thislist.append(i.emp_perfrev_no)
    thisdict={}
    i=0
    #creat a dictionary for all car numbers for display
    for x in thislist:
        while i<len(thislist):
            y = str(i)
            thisdict["emp_perfrev_no"+y] = thislist[i]
            i+=1

        
    return render(request,'providerassessments_due.html',{'thisdict':thisdict})





@allowed_users(allowed_roles=['Auditor'])
def Verify_providerassessments(request,pk_test):
    open_car=mod9001_providerassessment.objects.get(emp_perfrev_no=pk_test)
    form=Verifyeproviderassessments(instance=open_car)
    if request.method=="POST":
            #print("request.POST['qmsstatus']",request.POST['qmsstatus'])
            
            if request.POST['qmsstatus'] =="Rejected":
                request.POST=request.POST.copy()
                request.POST['status'] = 1 #requires approval first before next verification
                request.POST['verification']=2 #default verifiaction to Not effective
                print("request", request.POST)
            
            elif request.POST['qmsstatus'] == '1':
                #print("request.POST['qmsstatus']",request.POST['qmsstatus'])
                request.POST=request.POST.copy()
                request.POST['status'] = 1 # keep status approved
                request.POST['verification_status']='Closed'
            
            else:
                request.POST=request.POST.copy()






            form=Verifyeproviderassessments(request.POST, instance=open_car)
            if form.is_valid():
                form.save()
                return redirect('/providerassessments_due/')

    context={'form':form}  


    return render(request,'providerassesment_verify.html',context)


@login_required(login_url='login')
def providerassesment_7daysToExpiryview(request,pk_test):

    products=mod9001_providerassessment.objects.filter(emp_perfrev_no=pk_test)
    return render(request,'providerassesment_view_7_days_To_expiry.html',{'products':products})

def car_no():
   return str("TEGA-CAR-Q-"+(date.today()).strftime("%d%m%Y"))+str(randint(0, 999))

#########################CORRECTIVE ACTION##################################
@login_required(login_url='login')
@allowed_users(allowed_roles=['CorrectiveActionRequestor'])
def correctiveaction(request):
              
    form=corrective_action(initial={'car_no': car_no()})
                          
    if request.method=="POST":

        request.POST=request.POST.copy()
        request.POST['entered_by'] = request.user
        request.POST['date_today']=date.today()
        #request.POST['status'] = 5
        
        form=corrective_action(request.POST)
                        
        if form.is_valid():

                
            form.save()
            form=corrective_action(initial={'car_no': car_no()})
            context={'form':form}
            return render(request,'correctiveaction.html',context)
            
            
    context={'form':form}
    return render(request,'correctiveaction.html',context)

@login_required(login_url='login')
def correctiveaction_report(request):
    
    docmngr=mod9001_planning.objects.all() #get all corrective action in database 
    myFilter=correctiveactionFilter(request.GET, queryset=docmngr)
    docmngr=myFilter.qs
    if request.method=="POST":
        docmngr_list = mod9001_planning.objects.all()
        myFilter=correctiveactionFilter(request.GET, queryset=docmngr_list)
        docmngr=myFilter.qs
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="CorrectiveAction_register.csv"'

        writer = csv.writer(response)
        writer.writerow(['CAR No.', 'Date', 'Process', 'CAR Source','Reference','Element','Findings','Add. Desc.','RequestTo','Containment','RootCause','Action','Add.Details','ProposedBy','AssignedTo','When','Approval','Verification','Completion','Reschduled','Comment'])

    
        for i in docmngr:
            
            writer.writerow([i.car_no, i.car_no.date,i.car_no.process,i.car_no.car_source, i.car_no.reference,i.car_no.element,i.car_no.get_finding_display(),i.car_no.addesc,i.car_no.requesto,i.containment,i.rootcause,i.decision,i.details,i.proposedby,i.assignedto,i.due,i.status,i.qmsstatus,i.completion,i.scheduled,i.comment])
        return response
        
    else:
        return render(request,'CorrectiveAction_report.html',{'docmngr':docmngr,'myFilter':myFilter})



            
@login_required(login_url='login')
def planning(request):
              
    form=mod9001planning()
                          
    if request.method=="POST":

        request.POST=request.POST.copy()
        request.POST['entered_by'] = request.user
        request.POST['date_today']=date.today()
        request.POST['status'] = 5
        
        form=mod9001planning(request.POST)
                        
        if form.is_valid():

                
            form.save()
            form=mod9001planning()
            context={'form':form}
            return render(request,'planning.html',context)
            
            
    context={'form':form}
    return render(request,'planning.html',context)
#######################APPROVE PLANNING###################################################
@login_required(login_url='login')
def planning_pending(request):
    pendingcar=mod9001_planning.objects.filter(status='5') #get all planning  pending approval    
    #pendingcar=mod9001_correctiveaction.objects.all()#get all from corrective action table   
 
    
    context={'pendingcar':pendingcar} 
    return render(request,'planning_pending.html',context)



@login_required(login_url='login')
def approve_planning(request,pk_test):
    pending_planning=mod9001_planning.objects.get(car_no=pk_test)
    form=ApprovePlanning(instance=pending_planning)

    if request.method=="POST":

            
            
            request.POST=request.POST.copy()
            request.POST['approved_by']=request.user
            request.POST['approval_date']=date.today()                      

            form=ApprovePlanning(request.POST, instance=pending_planning)
            if form.is_valid():
                form.save()
                return redirect('/planning_pending/')

    context={'form':form}  


    return render(request,'planning_approve.html',context)    
#####################VERIFY PLANNING ########################################
def CARnumbers_7days_expire(*x):
    date_str = x[0]
    date_object = datetime.strptime(date_str, '%m/%d/%Y').date()
    delta =date_object - date.today()
    return delta.days

@login_required(login_url='login')
def planning_due(request):
    carExpire7days=mod9001_planning.objects.filter(status=1).filter(~Q(qmsstatus=1))
    thislist = []
   
    for i in carExpire7days:
        w=i.due
        t=w.strftime('%m/%d/%Y')
        if CARnumbers_7days_expire(t)<0:
            thislist.append(i.car_no)
    thisdict={}
    i=0
    #creat a dictionary for all car numbers for display
    for x in thislist:
        while i<len(thislist):
            y = str(i)
            thisdict["car_no"+y] = thislist[i]
            i+=1

        
    return render(request,'planning_due.html',{'thisdict':thisdict})



@login_required(login_url='login')
def planning_7daysToExpiryview(request,pk_test):

    products=mod9001_planning.objects.filter(car_no=pk_test)
    return render(request,'planning_view_7_days_To_expiry.html',{'products':products})

@allowed_users(allowed_roles=['Auditor'])
def verify_planning(request,pk_test):

    open_car=mod9001_planning.objects.get(car_no=pk_test)
    form=VerifyPlanning(instance=open_car)
    if request.method=="POST":
            #print("request.POST['verification']",request.POST['qmsstatus'])
            
            if request.POST['qmsstatus'] =="Rejected":
                request.POST=request.POST.copy()
                request.POST['status'] = 5 #requires approval first before next verification
                request.POST['verification']=2 #default verifiaction to Not effective
                #print("request", request.POST)
            
            elif request.POST['qmsstatus'] == '1':
                #print("request.POST['qmsstatus']",request.POST['qmsstatus'])
                request.POST=request.POST.copy()
                request.POST['status'] = 1 # keep status approved
                request.POST['verification_status']='Closed'
            
            else:
                request.POST=request.POST.copy()






            form=VerifyPlanning(request.POST, instance=open_car)
            if form.is_valid():
                form.save()
                return redirect('/planning_due/')

    context={'form':form}  


    return render(request,'planning_verify.html',context) 
          
###########################CHANGE REQUEST###########################################       
def req_no():
   return str("Comp-RFC-Q-"+(date.today()).strftime("%d%m%Y"))+str(randint(0, 999))



@login_required(login_url='login')
@allowed_users(allowed_roles=['ChangeRequestor'])
def changerequest(request):
              
    form=change_request(initial={'req_no': req_no()})
                          
    if request.method=="POST":

        request.POST=request.POST.copy()
        request.POST['entered_by'] = request.user
        request.POST['date_today']=date.today()
        request.POST['status'] = 5
        
        form=change_request(request.POST)
        print(request.POST)                
        if form.is_valid():

                
            form.save()
            form=change_request(initial={'req_no': req_no()})
            context={'form':form}
            return render(request,'changerequest.html',context)
            
            
    context={'form':form}
    return render(request,'changerequest.html',context)

@login_required(login_url='login')
def changeRegister_report(request):
    
    docmngr=mod9001_changeRegister.objects.all() #get all customer satisfaction in database 
    myFilter=changeRegisterFilter(request.GET, queryset=docmngr)
    docmngr=myFilter.qs
    if request.method=="POST":
        docmngr_list = mod9001_changeRegister.objects.all()
        myFilter=changeRegisterFilter(request.GET, queryset=docmngr_list)
        docmngr=myFilter.qs
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Change_Request.csv"'

        writer = csv.writer(response)
        writer.writerow(['RequestNo.', 'Date', 'RaisedBy', 'CARsource','Process','ChangeType','ChangeDesc.','Evaluation','Eval.Desc.','Cost','Currency','CostDesc.','Add.Desc.','Approved','Verified','ProposedBy','AssignedTo','When'])

    
        for i in docmngr:
            
            writer.writerow([i.req_no, i.date,i.raisedby,i.trigger,i.process,i.changetype,i.changedesc,i.get_evaluation_display(),i.evaldesc,i.cost,i.get_currency_display(),i.costdescription,i.add_desc,i.status,i.qmsstatus,i.proposedby,i.assignedto,i.due])
        return response
        
    else:
        return render(request,'changeRequest_report.html',{'docmngr':docmngr,'myFilter':myFilter})







#######################CHANGE REQUEST###################################################
@login_required(login_url='login')
def changerequest_pending(request):
    pendingcar=mod9001_changeRegister.objects.filter(status='5') #get all planning  pending approval    
    context={'pendingcar':pendingcar} 
    return render(request,'changerequest_pending.html',context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['TopManager'])
def approve_changerequest(request,pk_test):
    pending_planning=mod9001_changeRegister.objects.get(req_no=pk_test)
    form=ApproveChangeRequest(instance=pending_planning)

    if request.method=="POST":

            
            
            request.POST=request.POST.copy()
            request.POST['approved_by']=request.user
            request.POST['approval_date']=date.today()                      

            form=ApproveChangeRequest(request.POST, instance=pending_planning)
            if form.is_valid():
                form.save()
                return redirect('/changerequest_pending/')

    context={'form':form}  


    return render(request,'changerequest_approve.html',context) 

#####################VERIFY CHANGE REQUEST ########################################
@login_required(login_url='login')
def changerequest_due(request):
    carExpire7days=mod9001_changeRegister.objects.filter(status=1).filter(~Q(qmsstatus=1))
    thislist = []
   
    for i in carExpire7days:
        w=i.due
        t=w.strftime('%m/%d/%Y')
        if CARnumbers_7days_expire(t)<0:
            thislist.append(i.req_no)
    thisdict={}
    i=0
    #creat a dictionary for all car numbers for display
    for x in thislist:
        while i<len(thislist):
            y = str(i)
            thisdict["req_no"+y] = thislist[i]
            i+=1

        
    return render(request,'changerequest_due.html',{'thisdict':thisdict})



@login_required(login_url='login')
def changerequest_7daysToExpiryview(request,pk_test):

    products=mod9001_changeRegister.objects.filter(req_no=pk_test)
    return render(request,'changerequest_view_7_days_To_expiry.html',{'products':products})

@allowed_users(allowed_roles=['Auditor'])
def verify_changerequest(request,pk_test):

    open_car=mod9001_changeRegister.objects.get(req_no=pk_test)
    form=Verifychangerequest(instance=open_car)
    if request.method=="POST":
            #print("request.POST['verification']",request.POST['qmsstatus'])
            
            if request.POST['qmsstatus'] =="Rejected":
                request.POST=request.POST.copy()
                request.POST['status'] = 5 #requires approval first before next verification
                request.POST['verification']=2 #default verifiaction to Not effective
                #print("request", request.POST)
            
            elif request.POST['qmsstatus'] == '1':
                #print("request.POST['qmsstatus']",request.POST['qmsstatus'])
                request.POST=request.POST.copy()
                request.POST['status'] = 1 # keep status approved
                request.POST['verification_status']='Closed'
            
            else:
                request.POST=request.POST.copy()






            form=Verifychangerequest(request.POST, instance=open_car)
            if form.is_valid():
                form.save()
                return redirect('/changerequest_due/')

    context={'form':form}  


    return render(request,'changerequest_verify.html',context) 
########################### CUSTOMER COMPLAINT##################################
@login_required(login_url='login')
@allowed_users(allowed_roles=['RelationsManager'])
def customercomplaint(request):
              
    form=customer_complaint(initial={'comp_no': comp_no()})
                          
    if request.method=="POST":

        request.POST=request.POST.copy()
        request.POST['entered_by'] = request.user
        request.POST['date_today']=date.today()
        request.POST['status'] = 1
        
        form=customer_complaint(request.POST)
                        
        if form.is_valid():

                
            form.save()
            form=customer_complaint(initial={'comp_no': comp_no()})
            context={'form':form}
            return render(request,'customercomplaint.html',context)
            
            
          
        
    context={'form':form}
    return render(request,'customercomplaint.html',context)

@login_required(login_url='login')
def customer_complaint_report(request):
    
    docmngr=mod9001_customerComplaint.objects.all() #get all customer satisfaction in database 
    myFilter=customer_complaintFilter(request.GET, queryset=docmngr)
    docmngr=myFilter.qs
    if request.method=="POST":
        docmngr_list = mod9001_customerComplaint.objects.all()
        myFilter=customer_complaintFilter(request.GET, queryset=docmngr_list)
        docmngr=myFilter.qs
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="customer_complaint_register.csv"'

        writer = csv.writer(response)
        writer.writerow(['ComplaintNo.', 'Date', 'Time', 'complainant','Organisation','Process','CompalintType','Desc.','Classification','Correction','Add. Desc.','AssignedTo','When','Approved','Verified'])

    
        for i in docmngr:
            
            writer.writerow([i.comp_no, i.date,i.time,  i.complaint,i.organisation,i.process,i.type,i.complaint_desc,i.classification,i.correction,i.add_desc,i.assignedto,i.due,i.status,i.qmsstatus])
        return response
        
    else:
        return render(request,'customerComplaint_report.html',{'docmngr':docmngr,'myFilter':myFilter})








@login_required(login_url='login')
def customercomplaint_due(request):
    carExpire7days=mod9001_customerComplaint.objects.filter(status=1).filter(~Q(qmsstatus=1))
    #carExpire7days=mod9001_providerassessment.objects.filter(status=1)
    thislist = []
    for i in carExpire7days:
        #print("printing",i)
        w=i.due
        t=w.strftime('%m/%d/%Y')
        if CARnumbers_7days_expire(t)<0:
            thislist.append(i.comp_no)
    thisdict={}
    i=0
    #creat a dictionary for all car numbers for display
    for x in thislist:
        while i<len(thislist):
            y = str(i)
            thisdict["comp_no"+y] = thislist[i]
            i+=1

        
    return render(request,'customerComplaint_due.html',{'thisdict':thisdict})





@allowed_users(allowed_roles=['Auditor'])
def Verify_customercomplaint(request,pk_test):
    open_car=mod9001_customerComplaint.objects.get(comp_no=pk_test)
    form=Verifycustomer_complaint(instance=open_car)
    if request.method=="POST":
            #print("request.POST['qmsstatus']",request.POST['qmsstatus'])
            
            if request.POST['qmsstatus'] =="Rejected":
                request.POST=request.POST.copy()
                request.POST['status'] = 1 #requires approval first before next verification
                request.POST['verification']=2 #default verifiaction to Not effective
                print("request", request.POST)
            
            elif request.POST['qmsstatus'] == '1':
                #print("request.POST['qmsstatus']",request.POST['qmsstatus'])
                request.POST=request.POST.copy()
                request.POST['status'] = 1 # keep status approved
                request.POST['verification_status']='Closed'
            
            else:
                request.POST=request.POST.copy()






            form=Verifycustomer_complaint(request.POST, instance=open_car)
            if form.is_valid():
                form.save()
                return redirect('/customercomplaint_due/')

    context={'form':form}  


    return render(request,'customercomplaint_verify.html',context)


@login_required(login_url='login')
def customercomplaint_7daysToExpiryview(request,pk_test):

    products=mod9001_customerComplaint.objects.filter(comp_no=pk_test)
    return render(request,'customercomplaint_view_7_days_To_expiry.html',{'products':products})

##########################CUSTOMER SATISFACTION########################################

@login_required(login_url='login')
@allowed_users(allowed_roles=['RelationsManager'])
def customersatisfaction(request):
    form=customer_satisfaction(initial={'satis_no': satis_survey_no()})
    
              
                            
    if request.method=="POST":
        request.POST=request.POST.copy()
        request.POST['entered_by']=request.user
        request.POST['date_today']=date.today()
        request.POST['status'] = 1
#        #print("TEXT",request.POST)
##########################GET RANK DESCRIPTION FROM RATING SUBSTRING#####################################
        if "Poor" in request.POST['rank']:
            request.POST['rankdesc_survey'] = "Poor"
        elif "Improvement" in request.POST['rank']:
            request.POST['rankdesc_survey'] = "Improvement"
     
        elif "Satisfactory" in request.POST['rank']:
            request.POST['rankdesc_survey'] = "Satisfactory"
        
        elif "Good" in request.POST['rank']:
            request.POST['rankdesc_survey'] = "Good"
        
        elif "Excellent" in request.POST['rank']:
            request.POST['rankdesc_survey'] = "Excellent"
        
        else:
            pass
####################END#######################################

        
        form=customer_satisfaction(request.POST)
                        
        if form.is_valid():

                
            form.save()
            form=customer_satisfaction()
            context={'form':form}
            return render(request,'customersatisfaction.html',context)

            
            
          
        
    context={'form':form,'providers':providers}
    return render(request,'customersatisfaction.html',context)


@login_required(login_url='login')
def customersatisfaction_due(request):
    carExpire7days=mod9001_customerSatisfaction.objects.filter(status=1).filter(~Q(qmsstatus=1))
    #carExpire7days=mod9001_providerassessment.objects.filter(status=1)
    thislist = []
    for i in carExpire7days:
        #print("printing",i)
        w=i.due
        t=w.strftime('%m/%d/%Y')
        if CARnumbers_7days_expire(t)<0:
            thislist.append(i.satis_no)
    thisdict={}
    i=0
    #creat a dictionary for all car numbers for display
    for x in thislist:
        while i<len(thislist):
            y = str(i)
            thisdict["satis_no"+y] = thislist[i]
            i+=1

        
    return render(request,'customersatisfaction_due.html',{'thisdict':thisdict})





@allowed_users(allowed_roles=['Auditor'])
def Verify_customersatisfaction(request,pk_test):
    open_car=mod9001_customerSatisfaction.objects.get(satis_no=pk_test)
    form=Verifyecustomersatisfaction(instance=open_car)
    if request.method=="POST":
            #print("request.POST['qmsstatus']",request.POST['qmsstatus'])
            
            if request.POST['qmsstatus'] =="Rejected":
                request.POST=request.POST.copy()
                request.POST['status'] = 1 #requires approval first before next verification
                request.POST['verification']=2 #default verifiaction to Not effective
                print("request", request.POST)
            
            elif request.POST['qmsstatus'] == '1':
                #print("request.POST['qmsstatus']",request.POST['qmsstatus'])
                request.POST=request.POST.copy()
                request.POST['status'] = 1 # keep status approved
                request.POST['verification_status']='Closed'
            
            else:
                request.POST=request.POST.copy()






            form=Verifyecustomersatisfaction(request.POST, instance=open_car)
            if form.is_valid():
                form.save()
                return redirect('/customersatisfaction_due/')

    context={'form':form}  


    return render(request,'customersatisfaction_verify.html',context)


@login_required(login_url='login')
def customersatisfaction_7daysToExpiryview(request,pk_test):

    products=mod9001_customerSatisfaction.objects.filter(satis_no=pk_test)
    return render(request,'customersatisfaction_view_7_days_To_expiry.html',{'products':products})



@login_required(login_url='login')
def customersatisfaction_report(request):
    
    docmngr=mod9001_customerSatisfaction.objects.all() #get all customer satisfaction in database 
    myFilter=customerSatisfactionFilter(request.GET, queryset=docmngr)
    docmngr=myFilter.qs
    if request.method=="POST":
        docmngr_list = mod9001_customerSatisfaction.objects.all()
        myFilter=customerSatisfactionFilter(request.GET, queryset=docmngr_list)
        docmngr=myFilter.qs
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="customerSatisfaction_register.csv"'

        writer = csv.writer(response)
        writer.writerow(['SurveyNo.', 'Createdon', 'Organisation', 'Start','End','ResponseTime','ResolutionTime','DeliveryTime','Communication','Complaint','Quality','Info.Security','CustomerService','Rank','Comment','ImprovementPlan','Details','AssignedTo','When','Approved','Verified'])

    
        for i in docmngr:
            
            writer.writerow([i.satis_no, i.date,i.organisation,  i.start,i.end,i.responsetime,i.resolution,i.delivery,i.communication,i.compliant,i.quality,i.infosecurity,i.customerservice,i.rank,i.comment,i.improvplan,i.details,i.assignedto,i.due,i.status,i.qmsstatus])
        return response
        
    else:
        return render(request,'customerSatisfaction_report.html',{'docmngr':docmngr,'myFilter':myFilter})
