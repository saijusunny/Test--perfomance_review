from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from .models import Staff,Users,feedback,performance
from . import models
from  django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import os
from django.http import JsonResponse,HttpResponse
from django.contrib.auth import get_user_model

# Create your views here.
def login(request):
    return render(request,'login.html')
def signup(request):
    return render(request, 'signup.html')

@login_required(login_url='login')
def trans(request):
    ids=request.user.id
    if request.user.role=="USER":
        filt=Users.objects.get(id=ids) 
    else:
        filt=Staff.objects.get(id=ids)
    dats=Users.objects.filter(role="USERS")
    stf="STAFF"
    context={
        'filt':filt,
        "stf":stf,
        "dats":dats
    }

    return render(request, 'employee.html',context)

@login_required(login_url='login')
def home(request):
    ids=request.user.id
    filt=Users.objects.get(id=ids)
    stf="STAFF"
    adm="ADMIN"
    return render(request, 'home.html',{'filt':filt,"stf":stf,"adm":adm})


@login_required(login_url='login')
def home2(request):
    ids=request.user.id
    filt=Users.objects.get(id=ids)
    stf="STAFF"
    adm="ADMIN"
    return render(request, 'home_user.html',{'filt':filt,"stf":stf,"adm":adm})


def usercreate(request):
    if request.method=="POST":
        fname=request.POST['first_name']
        lname=request.POST['last_name']
        username=request.POST['username']
        password=request.POST['password']
        cpass=request.POST['cpassword']
        email=request.POST['email']  
        post=request.POST['post']
        salary=request.POST['salary']
        role=request.POST['role']
        
        if request.FILES.get('file') is not None:
            image=request.FILES.get('file')
        else:
            image = "static/image/icon.png"
       
        if role=="Staff":
         
            if password==cpass:
                if Staff.objects.filter(username=username).exists():
                    messages.info(request, 'This Username Is Already Exists!!!!!')
                    return redirect('signup')
                else:
                    user=Staff.objects.create_user(
                        first_name=fname,
                        last_name=lname,
                        username=username,
                        password=password,
                        email=email,
                        salary=salary,
                        post=post,
                        image=image,
                    )
                    user.save()
            else:
                messages.info(request, 'Password doesnot match!!!!!')
                return redirect('signup')
        else:
            if password==cpass:
                if Users.objects.filter(username=username).exists():
                    messages.info(request, 'This Username Is Already Exists!!!!!')
                    return redirect('signup')
                else:
                    user=Users.objects.create_user(
                        first_name=fname,
                        last_name=lname,
                        username=username,
                        password=password,
                        email=email,
                        salary=salary,
                        post=post,
                        image=image,
                    )
                    user.save()
            else:
                messages.info(request, 'Password doesnot match!!!!!')
                return redirect('signup')

        return redirect('login')
    else:
        return redirect('signup')


def adminlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                auth.login(request,user) 

                user_dt=Staff.objects.get(id=request.user.id)
                
                if user_dt.role=="STAFF":
                    return redirect('home')
                else:
                    return redirect('home2')
        else:
            messages.info(request, 'invalid username and password, try again')
            return redirect('login')
    else:
        return redirect('login')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def editpro(request,pk):
    
    if request.method=='POST':
        stf = Users.objects.get(id=pk)
        fname=request.POST.get('first_name')
        lname=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        cpass=request.POST.get('cpassword')
        email=request.POST.get('email')
        if password=="":
            created = Users.objects.filter(id=pk).update(first_name=fname,last_name=lname,username=username,email=email)
                
            return redirect('view_user',pk)
        else:

            if password==cpass:
                if password=="":
                    
                    created = Users.objects.filter(id=pk).update(first_name=fname,last_name=lname,username=username,email=email)
                    
                    return redirect('view_user',pk)
                else:
                    
                    created = Users.objects.filter(id=pk).update(last_name=lname,username=username,email=email)
                    u = Users.objects.get(id=pk)
                    u.set_password(password)
                    u.save() 
                    return redirect('view_user',pk)
            else:
                messages.info(request,f"Check Entered Password And Confirm Password")
                return redirect('view_user',pk)
 
    return redirect("view_user")

@login_required(login_url='login')
def add_performance(request,id):
    if request.method == 'POST':
            snd=performance.objects.create(
                user=request.user,
                emp_name = request.POST['emp_name'],
                emp_id = id,
                percentage = request.POST['percentage'],
                workdetails=request.POST['workdetails'],
                date= request.POST['date'],
            )
            snd.save()
            return redirect("view_user",id)
    return redirect("view_user")

@login_required(login_url='login')
def get_det_per(request):

        global idst
        idst = request.GET.get('ldg')
        items=performance.objects.get(id=idst)
        emp_name=items.emp_name
        workdetails=items.workdetails
        percentage=items.percentage
        date=items.date
        return JsonResponse({"status":" not","emp_name":emp_name,"workdetails":workdetails,"percentage":percentage,"date":date})
   
@login_required(login_url='login')
def edit_performance(request, id):
  
    if request.method == 'POST':
            items=performance.objects.get(id=idst)
            items.emp_name = request.POST['emp_name']
            items.percentage = request.POST['percentage']
            items.workdetails=request.POST['workdetails']
            items.date= request.POST['date']
            items.save()
            return redirect("view_user",id)
    return redirect("view_user")

@login_required(login_url='login')
def req_mny(request,id):
    if request.method == 'POST':
            snd=money.objects.create(
                user=request.user,
                name=request.POST['name'],
                accountno=request.POST['acc_no'],
                branch=request.POST['branch'],
                name2=request.POST['name2'],
                accountno2=request.POST['acc_no2'],
                branch2=request.POST['branch2'],
                ammount=request.POST['amount'],

            )
            snd.save()
            return redirect("trans")
    return redirect("trans")


@login_required(login_url='login')
def view_user(request,id):
    per_user=performance.objects.filter(emp_id=id)
    dats=Users.objects.get(id=id)
    emp=Staff.objects.filter(role="USERS")
    return render(request, "view_user.html", {"per_user":per_user,"dats":dats, "usr_id":id,"emp":emp})

@login_required(login_url='login')
def user_per(request):
    per_user=performance.objects.filter(emp_id=request.user.id)
    return render(request, 'user_per.html',{'per_user':per_user})

@login_required(login_url='login')
def send_feed(request):
    per_user=performance.objects.filter(emp_id=request.user.id)
    ass_emp=feedback.objects.get(person_id=request.user.id)
    us_det=Users.objects.get(id=ass_emp.assign_emp_id)
    return render(request, 'send_feedback.html',{'per_user':per_user,"ass_emp":us_det,"user_id":request.user.id})

@login_required(login_url='login')
def sav_assign(request,id):
    if request.method == 'POST':
            snd=feedback.objects.create(
                user=request.user,
                person_id=id,
                assign_emp_id=request.POST['assign_emp'],
            )
            snd.save()
            snds=feedback.objects.create(
                user=request.user,
                person_id=request.POST['assign_emp'],
                assign_emp_id=id,
            )
            snds.save()
            return redirect("view_user", id)
    return redirect("view_user", id)
    

@login_required(login_url='login')
def add_feed(request):
    if request.method == 'POST':
            snd=performance.objects.create(
                user=request.user,
                emp_name = request.POST['emp_name'],
                emp_id = request.POST['per_id'],
                percentage = request.POST['percentage'],
                workdetails=request.POST['workdetails'],
                date= request.POST['date'],
            )
            snd.save()
            return redirect("send_feed")
    return redirect("send_feed")


@login_required(login_url='login')
def up_pro(request,id):
    dele_data= Users.objects.get(id=id)
    dele_data.delete()
    return redirect("home")