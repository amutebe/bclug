@login_required(login_url='login')
def serviceRequest_pending_planning(request):

    products=mod20000_service_request.objects.filter(planning_flag='No')
    return render(request,'serviceRequest_pending_planning.html',{'products':products})




@login_required(login_url='login')
def serviceRequestPlanning(request,sr_id):

    form=serviceRequestPlanning(initial={'service_number':sr_id})
    #form=risk(initial={'risk_number': Risk_no(),'issue_number':issue_number})
              
                            
    if request.method=="POST":
        request.POST=request.POST.copy()
        request.POST['entered_by'] = request.user
        request.POST['date_today']=date.today()
        request.POST['status'] = 1
        #request.POST['status'] = 5
        
        form=serviceRequestPlanning(request.POST)
                        
        if form.is_valid():

                
            form.save()
            return redirect('/serviceRequest_pending_planning/')

            
            
          
        
    context={'form':form}
    return render(request,'service_request.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['IncidentManager'])
def incidentStaff(request):

    form=incident_RegisterStaff()
    #form=risk(initial={'risk_number': Risk_no(),'issue_number':issue_number})
              
                            
    if request.method=="POST":
        request.POST=request.POST.copy()
        request.POST['entered_by'] = request.user
        request.POST['date_today']=date.today()
        request.POST['status'] = 1
        #request.POST['status'] = 5
        
        form=incident_RegisterStaff(request.POST)
                        
        if form.is_valid():

                
            form.save()
            #form=incident_RegisterStaff()
            #context={'form':form}
            return redirect('/incidents_pending_analysis/')

            
            
          
        
    context={'form':form}
    return render(request,'incidentRegisterStaff.html',context)



@login_required(login_url='login')
def serviceRequest_due(request):
    carExpire7days=serviceRequestPlanning.objects.filter(status=1).filter(~Q(qmsstatus=1))
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

        
    return render(request,'serviceRequest_due.html',{'thisdict':thisdict})




@login_required(login_url='login')
def serviceRequest_7daysToExpiryview(request,pk_test):

    products=mod9001_incidentregisterStaff.objects.filter(incident_number=pk_test)
    return render(request,'incidentregister_view_7_days_To_expiry.html',{'products':products})





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





