from django.http import HttpResponse  
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func 

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            #print("Working",allowed_roles)
            group=[]
            i=0
            if request.user.groups.exists():
                for x in request.user.groups.all():

                    group.append(request.user.groups.all()[i].name)
                    #print(f"ALL GROUPS:{i} {group}")
                    
                    i+=1

            if request.user.groups.exists():
                for g in group:
                    print(g)
                    if g in allowed_roles:
                        return view_func(request,*args,**kwargs)

            
                return HttpResponse("You are not authorised")

            #if group in allowed_roles:
            #    return view_func(request,*args,**kwargs)
            #else:
            #    return HttpResponse("You are not authorised")
        return wrapper_func
    
    return decorator 
