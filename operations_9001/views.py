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

def document_no():
   return str("TEGA-Q-"+(date.today()).strftime("%d%m%Y"))+str(randint(0, 999))



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
def trainingReg(request):
    print("PRINTING PRINTING")        
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
        writer.writerow(['TainingNo','TrainingDescription.', 'AdditionalDescription', 'TrainingDate', 'Nature','Trainee','Dept','CompletionDate','Decision','NotEffective','Details','ActionPlan','AdditionalDesc.','AssignedTo','Timeline'])

    
        for i in trainingreg:
            
            writer.writerow([i.training_number, i.plan_number.description,i.plan_number.details,  i.train_date,i.get_nature_display(),i.trainee,i.trainee.dept,i.completion_date,i.get_decision_display(),i.reasonother,i.reasond,i.actionplan,i.actionplanother,i.assigned,i.timeline])
        return response
        
    else:
        return render(request,'Training_Evaluation_Report.html',{'trainingreg':trainingreg,'myFilter':myFilter})



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
        writer.writerow(['Incident. No.', 'Date', 'Time', 'Reference','ProcessName','Type','Description','Details','Classification','RootCause','Containment','AdditionalDescription','AsignedTo','DateAssigned','CompletionDate','CostDescription','LessonLearnt'])

    
        for i in incident:
            #if i.issue_number.get_context_display() is not None:#if the value is none django throws errors
            writer.writerow([i.incident_number, i.date,i.incident_number.time,i.incident_number.get_reference_display(),i.incident_number.processname,i.incident_number.incidentype,i.incident_number.incident_description,i.incident_number.other,i.classification,i.rootcause,i.get_correction_display(),i.description,i.assigned,i.date,i.completion,i.get_cost_display(),i.lesson])
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





@allowed_users(allowed_roles=['supervisor'])
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





@allowed_users(allowed_roles=['supervisor'])
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



            
            
          
        



