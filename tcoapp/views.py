from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from .forms import UpdateProfile,DocumentForm,Profilepic
from .models import userinfo, CreditUser
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import *
import random, string
from django.contrib.auth.decorators import login_required
from aws_admin import AWSAdmin
import csv
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import time
from django.core.urlresolvers import reverse
from silver.models.billing_entities.customer import Customer
from silver.models.billing_entities.provider import Provider
from silver.models.payments import Payment
from silver.models.plans import Plan,MeteredFeature
from silver.models.product_codes import ProductCode,Billing_ArchitectureType,Billing_Architecture,Billing_FeatureArchitecture
from silver.models.billing_entities.base import UserArchitectures
import urllib2
import json
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token
import json as simplejson
import requests

f = urllib2.urlopen('http://freegeoip.net/json/')
json_string = f.read()
f.close()
location = json.loads(json_string)
location_city = location['city']
location_state = location['region_name']
location_country = location['country_name']

def help(request):
    return render(request, 'help.html')

@login_required(login_url='/accounts/login/')
def Profile(request):
    user = User.objects.filter(id=request.user.id)
    phone=""
    custom=Customer.objects.filter(name=request.user.username)
    form = Profilepic(request.POST,request.FILES)
    print request.FILES
    if form.is_valid():
        cust=Customer.objects.get(name=request.user.username)
        cust.profile_img=form.cleaned_data['file']
        cust.save()
        print "image uploaded"
    else:
        form = Profilepic()
    return render(request,"profile-about.html",{'user':user,'custom':custom,"form":form})


@login_required(login_url='/accounts/login/')
def edit(request):
    formtype=request.GET.get("form_type")
    user={}
    if formtype=="Basic form":
        email=request.GET.get("email")
        username=request.GET.get("username")
        Customer.objects.filter(name=request.user.username).update(name=username)
        User.objects.filter(id=request.user.id).update(username=username,email=email)
        user=User.objects.filter(id=request.user.id)
   
    elif formtype=="Contact form":
        mobile=request.GET.get("mobile")
        twitter=request.GET.get("twitter")
        skype=request.GET.get("skype")

        Customer.objects.filter(name=request.user.username).update(phone_number=mobile,
            twitter=twitter,skype=skype)
    
    elif formtype=="Edit Address":
        city=request.GET.get("city")
        state=request.GET.get("state")
        pincode=request.GET.get("pincode")
        country=request.GET.get("country")
        Customer.objects.filter(name=request.user.username).update(city=city,state=state,zip_code=pincode,country=country)
   
    elif formtype=="Edit profilepic":
        profilepic=request.GET.get("profilepic")
        userinfo.objects.filter(user_id=32).update(profile_img=profilepic)
    return render(request,"profile-about.html",{'user':user})



@login_required(login_url='/accounts/login/')
def simple_upload(request):
    return HttpResponse(simplejson.dumps([True]))


@login_required(login_url='/accounts/login/')
def logout_page(request):
    ''' Logout '''
    logout(request)
    return redirect('/')


def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response   

def dashboard(request):
    return render(request,"profile-timeline.html")


def monitoring(request):
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    arch_url="http://"+request.get_host()+reverse("launched-architectures")
    architectures=requests.get(arch_url, headers={'Authorization': 'Token {}'.format(mytoken)})
    arch_json = architectures.json()
    return render(request,"profile-photos.html",{"arch_json" : arch_json})



def payment_conformation(request):
    archname=request.GET.get("archname")
    price=request.GET.get("price")
    print request.GET
    print archname
    print price
    price1=price.split("$")[1]
    UserArchitectures(username=request.user.username,
         price=price1,arch_name=archname).save()
    return HttpResponse("this is payment conformation")


def application(request):
    apptype=Billing_ArchitectureType.objects.filter(archtype="Application")
    app_image =  Billing_Architecture.objects.filter(archtype=apptype)   
    return render(request,"applications.html",{"apptype":apptype,"app":app_image})

def verticals(request):
    return render(request,"verticals.html")

def rest_main_architectures(request):
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    arch_url="http://"+request.get_host()+reverse("my-own-view")
    architectures=requests.get(arch_url, headers={'Authorization': 'Token {}'.format(mytoken)})
    arch_json = architectures.json()
    return render_to_response('architecture.html', {"arch_json" : arch_json})

def rest_arch_complete_info(request,pk):
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    arch_url="http://"+request.get_host()+reverse('ArchCompleInfo', kwargs={'pk':pk})
    architectures=requests.get(arch_url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    arch_json = architectures.json()
    print arch_json
    return render_to_response('arch_comple_info.html', {"arch_json" : arch_json})
    

def FtrdArchForArch(request,pk):
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    ftrd_arch_url="http://"+request.get_host()+reverse('FtrdArchByArchID', kwargs={'pk':pk})
    ftrd_architectures=requests.get(ftrd_arch_url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    ftrd_arch_json = ftrd_architectures.json()
    main_arch_url="http://"+request.get_host()+reverse('ArchCompleInfo', kwargs={'pk':pk})
    architectures=requests.get(main_arch_url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    main_arch_json = architectures.json()
    return render_to_response('featured_wizard.html',{'ftrd_arch_json': ftrd_arch_json,'main_arch_json':main_arch_json})

def CompleteFtrdArchInfo(request,pk):
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    url="http://"+request.get_host()+reverse('FtrdArchCompleInfo', kwargs={'pk':pk})
    info=requests.get(url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    arch_json = info.json()
    print arch_json
    return HttpResponse("this is testing")

def planspage(request,name):
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    url="http://"+request.get_host()+reverse('PayPlansInfo', kwargs={'name':name})
    info=requests.get(url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    payplans = info.json()
    return HttpResponse("this is testing")

def Launch_img(request,name):
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    url="http://"+request.get_host()+reverse('PlanByArchName', kwargs={'name':name})
    plans=requests.get(url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    plan_info=plans.json()
    arch_url="http://"+request.get_host()+reverse('Architectures_by_name', kwargs={'name':name})
    archs=requests.get(arch_url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    arch_info=archs.json()
    return render(request,"dynamic-side-img.html",{"plan_info":plan_info[0],
        'arch_info':arch_info[0]})

def PayementPlans(request,name):
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    url="http://"+request.get_host()+reverse('PlanByArchName', kwargs={'name':name})
    plans=requests.get(url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    plan_info=plans.json()
    arch_url="http://"+request.get_host()+reverse('Architectures_by_name', kwargs={'name':name})
    archs=requests.get(arch_url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    arch_info=archs.json()
    daily_plan_price=plan_info[0]['total_plan_price']/30
    Yearly_price=plan_info[0]['total_plan_price']*12
    return render(request,"plans_wizard.html",{"arch_info":arch_info[0],
        "plan_info":plan_info[0],"daily_plan_price":daily_plan_price,"Yearly_price":Yearly_price})


def invoicepage(request,name):
    plan_type=request.GET.get("plantype")
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    url="http://"+request.get_host()+reverse('PlanByArchName', kwargs={'name':name})
    plans=requests.get(url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    plan_info=plans.json()
    arch_url="http://"+request.get_host()+reverse('Architectures_by_name', kwargs={'name':name})
    archs=requests.get(arch_url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    arch_info=archs.json()
    date=time.strftime("%d/%m/%Y")
    instance_unit_price=0
    rds_unit_price=0
    s3_unit_price=0
    balancer_unit_price=0
    instance_total_price=0
    rds_total_price=0
    s3_total_price=0
    balancer_total_price=0
    total_price=0

    if plan_type=="daily":
        instance_unit_price=plan_info[0]['instance_cost']/30
        instance_total_price=(plan_info[0]['instance_cost']/30)*plan_info[0]['instance_count']
    
        rds_unit_price=plan_info[0]['rds_cost']/30
        rds_total_price=(plan_info[0]['rds_cost']/30)*plan_info[0]['rds_count']

        s3_unit_price=plan_info[0]['s3_cost']/30
        s3_total_price=(plan_info[0]['s3_cost']/30)*plan_info[0]['s3_count']

        balancer_unit_price=plan_info[0]['loadbalancer_cost']/30
        balancer_total_price=(plan_info[0]['loadbalancer_cost']/30)*plan_info[0]['balancer_count']

        total_price=plan_info[0]["total_plan_price"]/30

    if plan_type=="Yearly":
        instance_unit_price=plan_info[0]['instance_cost']*12
        instance_total_price=(plan_info[0]['instance_cost']*12)*plan_info[0]['instance_count']
    
        rds_unit_price=plan_info[0]['rds_cost']*12
        rds_total_price=(plan_info[0]['rds_cost']*12)*plan_info[0]['rds_count']

        s3_unit_price=plan_info[0]['s3_cost']*12
        s3_total_price=(plan_info[0]['s3_cost']*12)*plan_info[0]['s3_count']

        balancer_unit_price=plan_info[0]['loadbalancer_cost']*12
        balancer_total_price=(plan_info[0]['loadbalancer_cost']*12)*plan_info[0]['balancer_count']

        total_price=plan_info[0]["total_plan_price"]*12

    if plan_type=="Mothly":
        instance_unit_price=plan_info[0]['instance_cost']
        instance_total_price=(plan_info[0]['instance_cost'])*plan_info[0]['instance_count']
    
        rds_unit_price=plan_info[0]['rds_cost']
        rds_total_price=(plan_info[0]['rds_cost'])*plan_info[0]['rds_count']

        s3_unit_price=plan_info[0]['s3_cost']
        s3_total_price=(plan_info[0]['s3_cost'])*plan_info[0]['s3_count']

        balancer_unit_price=plan_info[0]['loadbalancer_cost']
        balancer_total_price=(plan_info[0]['loadbalancer_cost'])*plan_info[0]['balancer_count']
        total_price=plan_info[0]["total_plan_price"]

    return render(request, 'invoice.html',{"arch_info":arch_info[0],
        "plan_info":plan_info[0],
        "instance_unit_price":instance_unit_price,
        "rds_unit_price":rds_unit_price,
        "s3_unit_price":s3_unit_price,
        "balancer_unit_price":balancer_unit_price,
        "instance_total_price":instance_total_price,
        "rds_total_price":rds_total_price,
        "s3_total_price":s3_total_price,
        "balancer_total_price":balancer_total_price,
        "total_price":total_price,
        'date':date,
        "payment_type":plan_type
        })



def Featured_model_popup(request,name):
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    url="http://"+request.get_host()+reverse('PlanByArchName', kwargs={'name':name})
    plans=requests.get(url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    plan_info=plans.json()
    arch_url="http://"+request.get_host()+reverse('Architectures_by_name', kwargs={'name':name})
    archs=requests.get(arch_url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    arch_info=archs.json()
    return render(request,"ftrd_popup.html",{"plan_info":plan_info[0],
        'arch_info':arch_info[0]})