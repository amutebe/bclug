from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from. forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth import get_user_model
from .decorators import unauthenticated_user,allowed_users
from .filters import CarFilter
from django.contrib.auth.decorators import login_required
from datetime import date
import json
from django.db.models import Count, Q
import xlwt
from django.contrib.auth.models import User
from xlutils.copy import copy # http://pypi.python.org/pypi/xlutils
from xlrd import open_workbook # http://pypi.python.org/pypi/xlrd
import os
import csv

  

#function to get cars with 7 days to expire
def get_7days_expire(*x):
    date_str = x[0]
    date_object = datetime.strptime(date_str, '%m/%d/%Y').date()
    delta =date_object - date.today()
    return delta.days
    

#@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def home(request):
    #print('Hello djangox',request.user, request.user.id)
    total_tasks=car.objects.all().filter(status='4').filter(implementedby=request.user.id).count()
    print('Hello django',total_tasks)
 
    carstatus=car.objects.all().filter(~Q(verification=1)).order_by('car_date')[0:5] #get top 5 cars 
    cars=car.objects.all()
    customers=Customer.objects.all()
    total_cars=cars.count()
    total_approved=cars.filter(status='4').filter(~Q(verification=1)).count()
    total_pending=cars.filter(status='5').filter(~Q(verification=1)).count()
    #dump=ticket_class_view_3()
    carExpire7days=car.objects.filter(status=4).filter(~Q(verification=1)) #cars with  Status Open 
    count=0

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
    
#############################################################################
    categories = ['Total Pending','Total Approved','Total 7 days expiry','Total Due']
    survived_series_data = [total_pending,total_approved,counts,due]
        
    

    survived_series = {
        'name': 'CARs',
        'data': survived_series_data,
        'color': 'green'
    }

   

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'CAR by status'},
        'xAxis': {'categories': categories},
        'series': [survived_series],
        
    }

    dump = json.dumps(chart)
    
    
    context={'carstatus':carstatus,'cars':cars, 'customers':customers,'total_cars':total_cars,'total_approved':total_approved,'total_pending':total_pending,'counts':counts,'due':due,'chart': dump,'total_tasks':total_tasks}


 

    return render(request,'accounts/dashboard.html',context)

############# MSEM                   ##########################################
########FUNCTION TO FETCH CAR NON CONFORMITY LIST FROM NonConformityList TABLE BASED ON THE SOURCE SELECTED BY USER####

@login_required(login_url='login')
def car_approval(request):
    car_approval=car.objects.all()
    return render(request,'accounts/car_approve_form.html',{'car_approval':car_approval})


def CARerror(request):
    print("PRINTING MESSAGES",messages)
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
        print("PRINTING request.POST['entered_by']",request.POST['entered_by'])
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
        print("PRINTING",cars)
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
        print("PRINTING",products)
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
    editcar=car.objects.get(car_number=pk_test)
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









