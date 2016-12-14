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
from chatterbot import ChatBot

#from tcoapp.models import chat

f = urllib2.urlopen('http://freegeoip.net/json/')
json_string = f.read()
f.close()
location = json.loads(json_string)
location_city = location['city']
location_state = location['region_name']
location_country = location['country_name']


def help(request):
    return render(request, 'help.html')
def check(request):
    return render(request, 'check.html')


def warning(request):
    return render(request,'warning.html')


def host_step1(request):
    return render(request,'host_step1.html')

def host_step2(request):
    return render(request,'host_step2.html')           

def host_step3(request):
    return render(request,'host_step3.html')           

def host_step4(request):
    return render(request,'host_step4.html')           

def host_step5(request):
    return render(request,'host_step5.html')           

def host_step6(request):
    return render(request,'host_step6.html')           

def host_step7(request):
    return render(request,'host_step7.html')

def step7_53host(request):
    return render(request,'step7_53host.html')                 

def step7_cleanup_cloudfront(request):
    return render(request,'step7_cleanup_cloudfront.html')                 

def step7_cleanup_s3(request):
    return render(request,'step7_cleanup_s3.html')       

    


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

@login_required(login_url='/accounts/login/')
def dashboard(request):
    return render(request,"profile-timeline.html")

@login_required(login_url='/accounts/login/')
def monitoring(request):
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    arch_url="http://"+request.get_host()+reverse("launched-architectures")
    architectures=requests.get(arch_url, headers={'Authorization': 'Token {}'.format(mytoken)})
    arch_json = architectures.json()
    return render(request,"profile-photos.html",{"arch_json" : arch_json})


@login_required(login_url='/accounts/login/')
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

@login_required(login_url='/accounts/login/')
def application(request):
    apptype=Billing_ArchitectureType.objects.filter(archtype="Application")
    app_image =  Billing_Architecture.objects.filter(archtype=apptype)   
    return render(request,"applications.html",{"apptype":apptype,"app":app_image})

@login_required(login_url='/accounts/login/')
def verticals(request):
    return render(request,"verticals.html")

@login_required(login_url='/accounts/login/')
def rest_main_architectures(request):
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    arch_url="http://"+request.get_host()+reverse("my-own-view")
    architectures=requests.get(arch_url, headers={'Authorization': 'Token {}'.format(mytoken)})
    arch_json = architectures.json()
    plan_url="http://"+request.get_host()+reverse("AllplansInfo")
    plans=requests.get(plan_url, headers={'Authorization': 'Token {}'.format(mytoken)})
    plan_json = plans.json()

    for plan in plan_json:
        for arch in arch_json:
            if arch['architecture_name']==plan['product_code']:
                arch.update({'balancer_name':plan['balancer_name'],
                    'total_plan_price':plan['total_plan_price'],
                    'instance_count':plan['instance_count'],
                    'rds_count':plan['rds_count'],
                    's3_count':plan['s3_count'],
                    'balancer_count':plan['balancer_count'],
                    'rds_name':plan['rds_name'],
                    'balancer_name':plan['balancer_name'],
                    'rds_cost':plan['rds_cost'],
                    'loadbalancer_cost':plan['loadbalancer_cost'],
                    's3_cost':plan['s3_cost'],
                    's3_name':plan['s3_name'],
                    'instance_name':plan['instance_name'],
                    })
            else:
                pass
    

    print '***'*20
    print arch_json
    print '***'*20

    return render_to_response('architecture.html', {"arch_json" : arch_json})

@login_required(login_url='/accounts/login/')
def rest_arch_complete_info(request,pk):
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    arch_url="http://"+request.get_host()+reverse('ArchCompleInfo', kwargs={'pk':pk})
    architectures=requests.get(arch_url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    arch_json = architectures.json()
    print arch_json
    return render_to_response('arch_comple_info.html', {"arch_json" : arch_json})
    
@login_required(login_url='/accounts/login/')
def FtrdArchForArch(request,pk):
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    ftrd_arch_url="http://"+request.get_host()+reverse('FtrdArchByArchID', kwargs={'pk':pk})
    ftrd_architectures=requests.get(ftrd_arch_url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    ftrd_arch_json = ftrd_architectures.json()

    plan_url="http://"+request.get_host()+reverse("AllplansInfo")
    plans=requests.get(plan_url, headers={'Authorization': 'Token {}'.format(mytoken)})
    plan_json = plans.json()

    for plan in plan_json:
        for arch in ftrd_arch_json:
            if arch['architecture_name']==plan['product_code']:
                arch.update({'balancer_name':plan['balancer_name'],
                    'total_plan_price':plan['total_plan_price'],
                    'instance_count':plan['instance_count'],
                    'rds_count':plan['rds_count'],
                    's3_count':plan['s3_count'],
                    'balancer_count':plan['balancer_count'],
                    'rds_name':plan['rds_name'],
                    'balancer_name':plan['balancer_name'],
                    'rds_cost':plan['rds_cost'],
                    'loadbalancer_cost':plan['loadbalancer_cost'],
                    's3_cost':plan['s3_cost'],
                    's3_name':plan['s3_name'],
                    'instance_name':plan['instance_name'],
                    })
            else:
                pass

    print '***'*20
    print ftrd_arch_json
    print '***'*20
   

    main_arch_url="http://"+request.get_host()+reverse('ArchCompleInfo', kwargs={'pk':pk})
    architectures=requests.get(main_arch_url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    main_arch_json = architectures.json()

    return render_to_response('featurearch.html',{'ftrd_arch_json': ftrd_arch_json,'main_arch_json':main_arch_json})

@login_required(login_url='/accounts/login/')
def CompleteFtrdArchInfo(request,pk):
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    url="http://"+request.get_host()+reverse('FtrdArchCompleInfo', kwargs={'pk':pk})
    info=requests.get(url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    arch_json = info.json()
    print arch_json
    return HttpResponse("this is testing")

@login_required(login_url='/accounts/login/')
def planspage(request,name):
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    url="http://"+request.get_host()+reverse('PayPlansInfo', kwargs={'name':name})
    info=requests.get(url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    payplans = info.json()
    print payplans
    return HttpResponse("this is testing")

@login_required(login_url='/accounts/login/')
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

@login_required(login_url='/accounts/login/')
def PayementPlans(request,name):
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    url="http://"+request.get_host()+reverse('PlanByArchName', kwargs={'name':name})
    plans=requests.get(url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    plan_info=plans.json()
    arch_url="http://"+request.get_host()+reverse('Architectures_by_name', kwargs={'name':name})
    archs=requests.get(arch_url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    arch_info=archs.json()
    float("{0:.2f}".format(plan_info[0]['total_plan_price']))
    daily_plan_price=float("{0:.2f}".format(plan_info[0]['total_plan_price']/30))
    Yearly_price=float("{0:.2f}".format(plan_info[0]['total_plan_price']*12))
    monthly_price=float("{0:.2f}".format(plan_info[0]['total_plan_price']))
    
    print '***'*20
    print arch_info
    print '***'*20

    return render(request,"planarch.html",{"arch_info":arch_info[0],
        "plan_info":plan_info[0],"daily_plan_price":daily_plan_price,"Yearly_price":Yearly_price,'monthly_price':monthly_price})

@login_required(login_url='/accounts/login/')
def invoicepage(request,name,plan_type):
    plan_type=plan_type
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

        total_price=float("{0:.2f}".format(plan_info[0]["total_plan_price"]/30))

    if plan_type=="Yearly":
        instance_unit_price=plan_info[0]['instance_cost']*12
        instance_total_price=(plan_info[0]['instance_cost']*12)*plan_info[0]['instance_count']
    
        rds_unit_price=plan_info[0]['rds_cost']*12
        rds_total_price=(plan_info[0]['rds_cost']*12)*plan_info[0]['rds_count']

        s3_unit_price=plan_info[0]['s3_cost']*12
        s3_total_price=(plan_info[0]['s3_cost']*12)*plan_info[0]['s3_count']

        balancer_unit_price=plan_info[0]['loadbalancer_cost']*12
        balancer_total_price=(plan_info[0]['loadbalancer_cost']*12)*plan_info[0]['balancer_count']

        total_price= float("{0:.2f}".format(plan_info[0]["total_plan_price"]*12))

    if plan_type=="Mothly":
        instance_unit_price=plan_info[0]['instance_cost']
        instance_total_price=(plan_info[0]['instance_cost'])*plan_info[0]['instance_count']
    
        rds_unit_price=plan_info[0]['rds_cost']
        rds_total_price=(plan_info[0]['rds_cost'])*plan_info[0]['rds_count']

        s3_unit_price=plan_info[0]['s3_cost']
        s3_total_price=(plan_info[0]['s3_cost'])*plan_info[0]['s3_count']

        balancer_unit_price=plan_info[0]['loadbalancer_cost']
        balancer_total_price=(plan_info[0]['loadbalancer_cost'])*plan_info[0]['balancer_count']
         
        total_price=float("{0:.2f}".format(plan_info[0]["total_plan_price"]))

    return render(request, 'architecture_invoice.html',{"arch_info":arch_info[0],
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

@login_required(login_url='/accounts/login/')
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

# def bot(request):
#     chating=Chat.objects.all()
#     return render(request, 'chat.html',{"chating":chating})

# def chat_conversation(request):
#     usr_input=request.GET.get("input")
#     #usr_input="Good morning! How are you doing?"
#     if usr_input:
#         chatbot = ChatBot(
#         'Ron Obvious',
#         trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
#         )
#         chatbot.train("chatterbot.corpus.english")
#         bot_rply=chatbot.get_response(usr_input)
#         chating=Chat(user_id=request.user.id,
#         usermsg=usr_input,botmsg=bot_rply).save()    
#     else:
#         pass
#     chating=Chat.objects.all()
#     return render(request, 'conversation.html',{'chating':chating})



def chat_conversation(request):
    usr_input=request.GET.get("input")
    if usr_input:
        chatbot = ChatBot(
        'Ron Obvious',
        trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
        )
    #chatbot.train("chatterbot.corpus.english")
    bot_rply=chatbot.get_response(usr_input)
    return HttpResponse(bot_rply)

    # #usr_input="Good morning! How are you doing?"
    # if usr_input:
    #     chatbot = ChatBot(
    #     'Ron Obvious',
    #     trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
    #     )
    #     chatbot.train("chatterbot.corpus.english")
    #     bot_rply=chatbot.get_response(usr_input)
    #     chating=Chat(user_id=request.user.id,
    #     usermsg=usr_input,botmsg=bot_rply).save()    
    # else:
    #     pass
    #chating=Chat.objects.all()
    #return HttpResponse("this is text")
    #return render(request, 'conversation.html',{'chating':chating})

def Featured_popup(request,name):
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    url="http://"+request.get_host()+reverse('PlanByArchName', kwargs={'name':name})
    plans=requests.get(url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    plan_info=plans.json()
    arch_url="http://"+request.get_host()+reverse('Architectures_by_name', kwargs={'name':name})
    archs=requests.get(arch_url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    arch_info=archs.json()
    return render(request,"feature_archpopup.html",{"plan_info":plan_info[0],
        'arch_info':arch_info[0]})



def app_popup(request):
    return render(request, 'app_popup.html')
