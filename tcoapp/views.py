from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from .forms import Loginform,Registrationform,UpdateProfile,DocumentForm,Profilepic
from .models import userinfo, CreditUser
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import *
import random, string
from django.contrib.auth.decorators import login_required
import stripe
from aws_admin import AWSAdmin
import csv
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import time
from django.core.urlresolvers import reverse
# from paypal.standard.forms import PayPalPaymentsForm
from silver.models.billing_entities.customer import Customer
from silver.models.billing_entities.provider import Provider
from silver.models.payments import Payment
from silver.models.plans import Plan,MeteredFeature
from silver.models.product_codes import ProductCode,Billing_ArchitectureType,Billing_Architecture,Billing_FeatureArchitecture
from silver.models.billing_entities.base import UserArchitectures
import urllib2
import json

from django.core.files.storage import FileSystemStorage

from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token


# Automatically geolocate the connecting IP
f = urllib2.urlopen('http://freegeoip.net/json/')
json_string = f.read()
f.close()
location = json.loads(json_string)
location_city = location['city']
location_state = location['region_name']
location_country = location['country_name']
#location_zip = location['zipcode']


def getrds(archname):
    productname=ProductCode.objects.filter(value=archname)
    prdct=Plan.objects.get(product_code=productname)
    rds_unit_price=[]
    rds_name=[]
    rds_qry=None
    for prc in prdct.rds_metered_feature.all():
        rds_unit_price.append(prc.price_per_unit)
        rds_name.append(prc.Instance_Type)
        rds_qry=prdct.rds_count
    return [rds_name,rds_qry]


def gets3(archname):
    productname=ProductCode.objects.filter(value=archname)
    prdct=Plan.objects.get(product_code=productname)
    s3_name=[]
    s3_unit_price=[]
    s3_qty=None
    for prc in prdct.s3_metered_features.all():
        s3_name.append(prc.PriceDescription)
        s3_unit_price.append(prc.price_per_unit)
        s3_qty=prdct.s3_count
    return [s3_name,s3_qty]

def getload_balencer(archname):
    productname=ProductCode.objects.filter(value=archname)
    prdct=Plan.objects.get(product_code=productname)
    load_name=[]
    load_unit_price=[]
    load_qty=None
    for prc in prdct.LoadBalencer_metered.all():
        load_name.append(prc.PriceDescription)
        load_unit_price.append(prc.price_per_unit)
        load_qty=prdct.balancer_count
    return [load_name,load_qty]

def getec2(archname):
    ec2_unit_price=[]
    ec2_name=[]
    ec2_qry=None
    productname=ProductCode.objects.filter(value=archname)
    prdct=Plan.objects.get(product_code=productname)
    #prdct=get_product(archname)
    for prc in prdct.metered_features.all():
        ec2_unit_price.append(prc.price_per_unit)
        ec2_name.append(prc.name)
        ec2_qry=prdct.instance_count
    return [ec2_name,ec2_qry]




def get_ftrd_count(img_id):
    Billing_FeatureArchitecture.objects.filter(architecture_id=img_id).count()


def price_calculator(archname):
    productname=ProductCode.objects.filter(value=archname)
    try:
        price=Plan.objects.get(product_code=productname)
        ec2_unit_price=0
        rds_unit_price=0
        s3_unit_price=0
        load_unit_price=0
        ec2_qty=price.instance_count
        rds_qty=price.rds_count
        s3_qty=price.s3_count
        load_qty=price.balancer_count

        for prc in price.metered_features.all():
            ec2_unit_price=prc.price_per_unit

        for prc in price.rds_metered_feature.all():
            rds_unit_price=prc.price_per_unit

        for prc in price.s3_metered_features.all():
            s3_unit_price=prc.price_per_unit
        
        for prc in price.LoadBalencer_metered.all():
            load_unit_price=prc.price_per_unit

        price_product=((ec2_unit_price*ec2_qty)+(rds_unit_price*rds_qty)+(s3_unit_price*s3_qty)+(load_unit_price*load_qty))*24*30
        total_price_product=float("{0:.2f}".format(price_product))
    except:
        pass
    return total_price_product
    
 


def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))


# Create your views here.
# def IndexLogin(request):
#   #return HttpResponse("this is saple view")
#   return render(request, 'index.html')


def Login(request):
    error_message=""
    success_message = ""

    user = ""
    if request.method == 'POST':
        form = Loginform(request.POST)
        username = request.POST.get('email')
        password = request.POST['password']
        
        if form.is_valid():
            user = authenticate(username=username,password=password)
            print username
            print password
            print "*"*20
            print user
            if user:
                if user.is_active:
                    auth_login(request, user)
                    user_info=request.user
                    return redirect('/tco/architecture')
                else:
                    error_message ="Sorry your Account not activated,please conform your email" 
            else:
                error_message ="Username and Password did not match."
    else:
        form = Loginform()
    return render(request, 'login.html', {'form':form,
        'error_message':error_message, 'success_message':success_message})     


def Register(request):
    success_message = ""
    error_message = ""
    iam_user_data = ""

    form1 = Loginform()
    form = Registrationform()
    if request.method == 'POST':
        form = Registrationform(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            pwd =request.POST.get("password")
            mail = request.POST.get("email")
            phone_num=request.POST.get("phone_number")
            username_check=User.objects.filter(username=username)
            email_check=User.objects.filter(email=mail)
            if username_check:
                error_message="Username already exists"
                #return render(request, 'register.html', {'error_message':error_message, 'form':form})
            elif email_check:
                error_message="Email already exists"
                #return render(request, 'register.html', {'error_message':error_message, 'form':form})
            else:
                user = User.objects.create_user(username, mail, pwd)
                
                uid=""
                user_id = User.objects.filter(email=mail)
                for uinfo in user_id:
                    uid=uinfo.id
                
                cnfrm_code=randomword(20)
                cmfrm_link=cnfrm_code+str(uid)
                userinfo(user_id=uid,phone=phone_num,reg_cnrrm_code=cmfrm_link).save()

                deactivte_user = User.objects.filter(email=mail).update(is_active=0)

                
                ''' AWS USER CREATION '''
                # aws_admin = AWSAdmin()
                # user_path = "/"+username+"/"
                # iam_user = aws_admin.create_IAM(username, user_path)
                # iam_user_key = aws_admin.create_IAM_KEY(username)
                # print iam_user
                # print iam_user_key

                # iam_user_data = iam_user_key['AccessKey']
                # iam_user_accesskey = iam_user_data['AccessKeyId']
                # iam_user_secret_key = iam_user_data['SecretAccessKey']
                # iam_user_status = iam_user_data['Status']
                # print "&*"*20
                # print iam_user_accesskey
                # print iam_user_secret_key
                # print iam_user_status

                # userinfo.objects.filter(user_id=uid).update(iam_access_key=iam_user_accesskey,
                #     iam_secret_key=iam_user_secret_key, iam_status=iam_user_status)
                
                ''' Sending Email'''
                subject, from_email, to = 'Activate Your Cloud-TCO Account', 'vinod@ysec.io',[mail]
                text_content = 'Please confirm your email address to activate your Cloud-TCO account.'
                html_content = render_to_string("mymail.html",{'cmfrm_link':cmfrm_link})
                msg = EmailMultiAlternatives(subject, text_content, from_email, to)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                success_message = "You are Successfully Registered"
                

                '''Creating Customer in Billing Software'''
                Customer(name=username,address_1=location_city,state=location_state,country=location_country).save()
                
                return render(request, 'register.html',{'form': form,"success_message":success_message,})

    else:
        form = Registrationform()
    return render(request, 'register.html',{'form': form,"success_message":success_message,'error_message':error_message})
    

def Forgot(request):
    #print request.GET
    return render(request, 'forgot.html')

def help(request):
    #print request.GET
    return render(request, 'help.html')


def Forgotpwd(request):
    #print request.GET
    email=request.GET.get("forgot_email")
    uid=""

    email_check=User.objects.filter(email=email)
    for email in email_check:
        uid=email.id
    print 'email:',email
    if email_check:
        new_pwd=randomword(8)
        print '**'*20
        print new_pwd
        user = User.objects.get(id=uid)
        user.set_password(new_pwd)
        user.save()
    else:
        return HttpResponse("")
    return HttpResponse("New Password has been sent to your Email,Please Check and login with new password.")


@login_required(login_url='/accounts/login/')
def arcc(request):
    return render(request, 'arcc.html')

# def Profile(request):
#     #return HttpResponse("this is sample view")
#     return render(request, 'profile-about.html')
@login_required(login_url='/accounts/login/')
def test(request):
    #return HttpResponse("this is sample view")
    return render(request, 'architecture.html')

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
        print "*************************************"
        #print request.Files
        print profilepic

        userinfo.objects.filter(user_id=32).update(profile_img=profilepic)
    return render(request,"profile-about.html",{'user':user})






    # if username==curnt_username and email==curnt_email:

    #     print "**"*20
    #     print "username and email already exist"

    #     User.objects.filter(id=uid).update(username=username,email=email)
       
    #     if userinfo.objects.get(uid=uid):
    #         userinfo.objects.filter(user_id=uid).update(phone=mobile)
    #     else:
    #         userinfo(uid=uid,phone=mobile).save()
    #     return render(request,"profile-about.html",{'user':user,'phone':mobile})

    # elif username==curnt_username and email != curnt_email:
    #     print "**"*20
    #     print "username already exist and email not equl"
    #     if email_check:
    #         print "email check is alredy exists"
    #         return HttpResponse("Email already exists")    
    #     else:
    #         User.objects.filter(id=uid).update(username=username,email=email)

    #         if userinfo.objects.get(uid=uid):
    #             userinfo.objects.filter(user_id=uid).update(phone=mobile)
    #         else:
    #             userinfo(uid=uid,phone=mobile).save()

    #         # userinfo.objects.filter(user_id=uid).update(phone=mobile)
    # elif username!=curnt_username and email == curnt_email:
    #     print "**"*20
    #     print "username not equal and email equl"
    #     if username_check:
    #         return HttpResponse("Username already exists.")    
    #     else:
    #         User.objects.filter(id=uid).update(username=username,email=email)
    #         if userinfo.objects.get(uid=uid):
    #             userinfo.objects.filter(user_id=uid).update(phone=mobile)
    #         else:
    #             userinfo(uid=uid,phone=mobile).save()
    # elif username!=curnt_username and email != curnt_email:
    #     if username_check:
    #         return HttpResponse("Username already exists")    
    #     elif email_check:
    #         return HttpResponse("Email already exists")  
    #     else:
    #         User.objects.filter(id=uid).update(username=username,email=email)
    #         # userinfo.objects.filter(user_id=uid).update(phone=mobile)
    #         if userinfo.objects.get(uid=uid):
    #             userinfo.objects.filter(user_id=uid).update(phone=mobile)
    #         else:
    #             userinfo(uid=uid,phone=mobile).save()
    #     return render(request,"profile-about.html",{'user':user,'phone':phone})


    # # else:
    # #     User.objects.filter(id=uid).update(username=username,email=email)
    # #     userinfo.objects.filter(id=uid).update(phone=mobile)

    # return HttpResponse("this is testing")











# @login_required(login_url='/accounts/login/')
# def editcontact(request):
#    print request.GET
#    mobile=request.GET.get("mobile")
#    twitter=request.GET.get("twitter")
#    skype=request.GET.get("skype")

#    print "**"*20
#    print mobile
#    print twitter
#    print skype

#    user = User.objects.filter(id=request.user.id)
#    print "**"*20
#    print user
#    phone = ""
#    print request.user.id
#    user_info = userinfo.objects.filter(user_id=request.user.id)
#    for ph in user_info:
#         phone=ph.phone
#    return render(request,"profile-about.html",{'user':user,'phone':phone})

import json as simplejson

@login_required(login_url='/accounts/login/')
def simple_upload(request):


    print '***'*20
    print "this is upload"
    print request.POST
    print request.FILES

    return HttpResponse(simplejson.dumps([True]))


@login_required(login_url='/accounts/login/')
def logout_page(request):
    ''' Logout '''
    logout(request)
    return redirect('/')



@login_required(login_url='/accounts/login/')
def architecture_view(request):
    ''' Architecture View'''
    cldtype=Billing_ArchitectureType.objects.filter(archtype="cloud")
    apptype=Billing_ArchitectureType.objects.filter(archtype="Application")
    cloud_image = Billing_Architecture.objects.filter(archtype=cldtype)
    app_image =  Billing_Architecture.objects.filter(archtype=apptype)   
    arch_dict={}
    # for cld in cloud_image:
    #     dict1={"name":cld.architecture_name,
    #     "image":cld.architecture_img,
    #     "price":price_calculator(cld.architecture_name),
    #     "count":get_ftrd_count(cld.id)
    #     }
    #     arch_dict.update(dict1)
   
    # print '****'*20
    # print arch_dict
    #Billing_FeatureArchitecture.objects.filter(architecture_id=img_id)   
    #cloud_image = Architecture.objects.filter(archtype_id=1)
    #app_image = Architecture.objects.filter(archtype_id=2)    
    
    return render_to_response('architecture.html', {"image" : cloud_image,"app" : app_image,"arch_dict":arch_dict})

@login_required(login_url='/accounts/login/')
def feature_architecture_view(request, img_id):
    ''' Feature Architecture View'''
    
    image_all = Architecture.objects.all()
    arch = Architecture.objects.get(id=img_id)
    image = arch.architecture_img
    price = arch.price
    fea_image = FeatureArchitecture.objects.filter(architecture_id=img_id)
    return render_to_response('test2.html', {'image_list': fea_image, 'arch_image': image, 'image': image_all, 'price': price,},)

@login_required(login_url='/accounts/login/')
def architecture_launch(request, img_id):
    ''' Feature Architecture View'''
    image_id = ""
    image = ""
    image_price = ""
    image_name = ""

    fea_image = FeatureArchitecture.objects.filter(architecture_id=img_id)

    if fea_image:
        ''' If architecture images '''
        print "architecture image"
        arch_image_data = Architecture.objects.get(id=img_id)
        image_id = arch_image_data.id
        image = arch_image_data.architecture_img
        image_name = arch_image_data.architecture_name
        image_price = arch_image_data.price
    else:
        ''' If featured architecture images '''
        fea_image_data = FeatureArchitecture.objects.get(id=img_id)
        image_id = fea_image_data.id
        image = fea_image_data.feature_img
        image_name = fea_image_data.architecture_name
        image_price = fea_image_data.price


        print "feature img"
    # return HttpResponse("launching an instance")
    return render_to_response('test3.html', {'image_name': image_name, 'image': image,
        'image_price': image_price, 'image_id': image_id},)


def resetpwd(request):
    return render(request, 'resetpassword.html')


def resetpwd_ajax(request):
    #current_pwd=request.GET.get("currentpassword")
    new_pwd=request.GET.get("newpassword")
    confirm_pwd=request.GET.get("conformpassword")
    
    print "new_pwd",new_pwd
    print "confirm_pwd",confirm_pwd
    uid=request.user.id
    if new_pwd==confirm_pwd:
        print "**"*20
        print "both emails matched"
        user_pwd=""
        print "uid:",uid
        pwd_check=User.objects.filter(id=uid)
        print "uid:",uid
        user = User.objects.get(id=uid)
        print "uid:",uid
        user.set_password(new_pwd)
        user.save()
        user_login = authenticate(username=request.user.username,password=new_pwd)
        if user_login:
            if user_login.is_active:
                auth_login(request, user)
    else:
        print "not match"
        return HttpResponse("Password and conformpassword didn't Match.")

    return HttpResponse("Your Password Successfully Changed")



@login_required
def plans_view(request):    
    # plan_list = stripe.Plan.list(limit=3)
    # print plan_list

    # return HttpResponse("Payments")
    # return render('payments.html', { },)
    return render(request,"plans.html",{})

# @login_required
# def payment_view(request):

@login_required
def payment_view(request):
    price = ""
    print request.user
    user = request.user.id
    plan_type = request.GET.get('plan')
    print "@@#"*20

    print "plan", plan_type
    error_message = ""
    form = PaymentForm()
    # if request.method == "POST":
    #     form = PaymentForm(request.POST)
    #     if form.is_valid():
    #         card = request.POST.get("card_number")
    #         month = request.POST.get("expire_month")
    #         year = request.POST.get("expire_year")
    #         cvc = request.POST.get("cvc")  

    #         print card
    #         print month
    #         print year
    #         print cvc          
    # else:
    #     form = PaymentForm()

    email_id =  request.user.email
    if request.method == "GET":
        form1 = PaymentForm(request.GET)
        if form1.is_valid():
            card = request.GET.get("card_number")
            month = request.GET.get("expire_month")
            year = request.GET.get("expire_year")
            cvc = request.GET.get("cvc") 
            plan_type = request.GET.get("plan_type") 
            print card
            print month
            print year
            print cvc 
            print plan_type
            try:
                # creating stripe token
                token = stripe.Token.create(
                    card={
                        "number": card,
                        "exp_month": month,
                        "exp_year": year,
                        "cvc": cvc
                    },
                )
                print "#######"*20
                print token
                print "########"*20
                # Create a Stripe Customer
                customer = stripe.Customer.create(
                  source=token,
                  plan=plan_type,
                  email=email_id
                )   

                print "============"
                print user
                print customer.id
                print plan_type
                print "============="
                credit_user = CreditUser(user_id=user, stripe_id=customer.id,
                    plan_type=plan_type, card_number=card).save()

                # credit_user.save()
                print credit_user
                # last_4_digits = form.cleaned_data['last_4_digits'],
                #     stripe_id = customer.id,
                #     plan = plan_type

                # CreditUser

                # print "$$$$$$"*20
                # print customer.id
                # print plan_type
                # print "$$$$$$"*20

                success_message = "Stripe Customer Created"
                return HttpResponse("Stripe Customer Created")

            except stripe.error.CardError, e:
                print "card error"
                error_message = "You have entered wrong credit card details... !" 
                return render_to_response('test4.html', {'form': form, 'plan_type': plan_type, 'error_message': error_message},)                               
                # messages.info(request, (u"You have entered wrong credit card details ... !"))               
            except stripe.error.InvalidRequestError, e:
                print "invalid request error"
                error_message = "You have entered Invalid Request Error" 
                return render_to_response('test4.html', {'form': form, 'plan_type': plan_type, 'error_message': error_message},)
                # messages.info(request, (u"You have entered invalid request ... !"))             
                pass
            except stripe.error.AuthenticationError, e:
                print "AuthenticationError"
                error_message = "Stripe Authentication Error" 
                return render_to_response('test4.html', {'form': form, 'plan_type': plan_type, 'error_message': error_message},)
                # messages.info(request, (u"Your authentications failed due to stripe keys...!"))             
                # pass
            except stripe.error.APIConnectionError, e:
                print "api connection error"
                error_message = "API Connection Error, re enter the details...!" 
                return render_to_response('test4.html', {'form': form, 'plan_type': plan_type, 'error_message': error_message},)
                # messages.info(request, (u"Api connection error , re enter the details...!"))             
                # pass
            except stripe.error.StripeError, e:
                print "stripe error"
                error_message = "Some stripe traffic error , please provide the details again ...!" 
                return render_to_response('test4.html', {'form': form, 'plan_type': plan_type, 'error_message': error_message},)
                # messages.info(request, (u"Some stripe traffic error , please provide the details again ...!"))            
                # pass
            # except IntegrityError:
            #     print "integrity error"                                              
                # messages.info(request, (u"This User has already existed...!"))                
            except Exception, e:
                # print e
                print "global exception"
                error_message = "Please provide correct details... !" 
                return render_to_response('test4.html', {'form': form, 'plan_type': plan_type, 'error_message': error_message},)
                # messages.info(request, (u"Please provide correct details... !"))

                     
    else:
        form = PaymentForm()
        
    return render_to_response('test4.html', {'form': form, 'plan_type': plan_type, 'error_message': error_message},)
    # return HttpResponse("Payments")


@login_required
def key_download(request):
    ''' Download results in CSV Format  '''
    print request.user.id
    
    data = userinfo.objects.filter(user_id=request.user.id)    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename=%s.csv"%(request.user)
    writer = csv.writer(response)
    writer.writerow(['AccessKey', 'SecretKey'])
    for i in data:
        writer.writerow([i.iam_access_key, i.iam_secret_key])
    return response



def activate_usr(request,cnfrm_id):
    check_code=userinfo.objects.filter(reg_cnrrm_code=cnfrm_id)
    if check_code:
        actvt_id=cnfrm_id[-2:]
        User.objects.filter(id=int(actvt_id)).update(is_active=1)
    return render(request,"rgstr_activation.html")


def invoice(request):
    #archname=request.GET.get("plan_button")
    invoice_num="%06d"%request.user.id
    date=time.strftime("%d/%m/%Y")
    packtype=request.GET.get("packtype")
    print "***"*20
    print packtype

    archname=request.GET.get("name_arch")
    #archname="Model 1"
    mtrd_ftr_name=""
    productname=ProductCode.objects.filter(value=archname)
    price=Plan.objects.get(product_code=productname)
    ec2_unit_price=0
    rds_unit_price=0
    s3_unit_price=0
    ec2_qty=price.instance_count
    rds_qty=price.rds_count
    s3_qty=price.s3_count
    ec2_name=""
    rds_name=""
    s3_name=""
    single_unit_ec2_daily=None
    total_ec2=None
    single_rds=None
    total_rds=None
    single_s3=None
    total_s3=None
    grand_total=None
    total_load=None
    single_load=None
    load_unit_price=0
    load_qty=price.balancer_count
    load_name=""
    type_pay=""

    for prc in price.metered_features.all():
        ec2_unit_price=prc.price_per_unit
        ec2_name=prc.name
    for prc in price.rds_metered_feature.all():
        rds_unit_price=prc.price_per_unit
        rds_name=prc.Instance_Type

    for prc in price.s3_metered_features.all():
        s3_name=prc.PriceDescription
        s3_unit_price=prc.price_per_unit
    for prc in price.LoadBalencer_metered.all():
        load_name=prc.PriceDescription
        load_unit_price=prc.price_per_unit

    price_product=((ec2_unit_price*ec2_qty)+(rds_unit_price*rds_qty)+(s3_unit_price*s3_qty)+(load_unit_price*load_qty))*24*30
    total_price_product=float("{0:.2f}".format(price_product))
    
    if packtype=="daily":
        print "is is in condition"
        single_unit_ec2_daily=float("{0:.2f}".format((ec2_unit_price)*24))
        total_ec2=float("{0:.2f}".format((ec2_unit_price*ec2_qty)*24))
        single_rds=float("{0:.2f}".format((rds_unit_price)*24))
        total_rds=float("{0:.2f}".format((rds_unit_price*rds_qty)*24))
        single_s3=float("{0:.2f}".format((s3_unit_price)*24))
        total_s3= float("{0:.2f}".format((s3_unit_price*s3_qty)*24))
        single_load=float("{0:.2f}".format((load_unit_price)*24))
        total_load= float("{0:.2f}".format((load_unit_price*load_qty)*24))
        grand_total=float("{0:.2f}".format(total_price_product/30))
        type_pay="Daily"


    elif packtype=="Mothly":
        print "is is in condition"
        single_unit_ec2_daily=float("{0:.2f}".format((ec2_unit_price)*24*30))
        total_ec2=float("{0:.2f}".format((ec2_unit_price*ec2_qty)*24*30))
        single_rds=float("{0:.2f}".format((rds_unit_price)*24*30))
        total_rds=float("{0:.2f}".format((rds_unit_price*rds_qty)*24*30))
        single_s3=float("{0:.2f}".format((s3_unit_price)*24*30))
        total_s3= float("{0:.2f}".format((s3_unit_price*s3_qty)*24*30))
        single_load=float("{0:.2f}".format((load_unit_price)*24*30))
        total_load= float("{0:.2f}".format((load_unit_price*load_qty)*24*30))


        grand_total=float("{0:.2f}".format(total_price_product))
        type_pay="Monthly"

    elif packtype=="Yearly":
        print "is is in condition"
        single_unit_ec2_daily=float("{0:.2f}".format((ec2_unit_price)*24*30*12))
        total_ec2=float("{0:.2f}".format((ec2_unit_price*ec2_qty)*24*30*12))
        single_rds=float("{0:.2f}".format((rds_unit_price)*24*30*12))
        total_rds=float("{0:.2f}".format((rds_unit_price*rds_qty)*24*30*12))
        single_s3=float("{0:.2f}".format((s3_unit_price)*24*30*12))
        total_s3= float("{0:.2f}".format((s3_unit_price*s3_qty)*24*30*12))
        single_load=float("{0:.2f}".format((load_unit_price)*24*30*12))
        total_load= float("{0:.2f}".format((load_unit_price*load_qty)*24*30*12))

        grand_total=float("{0:.2f}".format(total_price_product*12))
        type_pay="Yearly"

    else:
        pass

    return render(request, 'invoice.html',{'invoice_num':invoice_num,
        'date':date,'archname':archname,"ec2_name":ec2_name,"rds_name":rds_name,
        "s3_name":s3_name,"ec2_qty":ec2_qty,"rds_qty":rds_qty,"s3_qty":s3_qty,
        "single_unit_ec2_daily":single_unit_ec2_daily,"single_rds":single_rds,
        "single_s3":single_s3,"total_ec2":total_ec2,"total_rds":total_rds,
        "total_s3":total_s3,"grand_total":grand_total,'total_load':total_load,
        "single_load":single_load,'load_name':load_name,"load_qty":load_qty,
        "type_pay":type_pay
        })


def cloud_process_wizard_view(request):
    image = Architecture.objects.all()
    return render(request,"wizard.html",{"image":image})


def featured_image_wizard(request):
    img_id=request.GET.get("img_id")
    #img_id=1
    arch = Billing_Architecture.objects.get(id=img_id)
    image = arch.architecture_img
    name=arch.architecture_name
    main_arch_price=price_calculator(name)

    fea_image = Billing_FeatureArchitecture.objects.filter(architecture_id=img_id)
    price_dict={}
    for ftrd in fea_image:
        ftrd_dict={ftrd.id:[
        ftrd.architecture_name,
        price_calculator(ftrd.architecture_name),
        ftrd.feature_img,
        getec2(ftrd.architecture_name),
        getrds(ftrd.architecture_name),
        getload_balencer(ftrd.architecture_name),
        gets3(ftrd.architecture_name),

        ]}
        price_dict.update(ftrd_dict)
        print '****'*20
    for k,v in price_dict.items():
        print k
        print "v[0]",v[0]
        print "v[1]",v[1]
        print "v[2]",v[2]
        print "v[3]",v[3]
        print "v[4]",v[4]
        print "v[5]",v[5]
        print "v[6]",v[6]

    return render_to_response('featured_wizard.html',{'image_list': fea_image,
     'arch_image': image,
        'name':name,
        'price_dict':price_dict,'main_arch_price':main_arch_price}
        )


def payments_wizard(request):
    #arch_info={}
    #arch_name="Model 2"
    arch_name=request.GET.get("name_arch")
    name=""
    price=""
    day_price=""
    month_price=""
    year_price=""
    image=""
    prodcut_name=ProductCode.objects.get(value=arch_name)
    arch_info=Billing_FeatureArchitecture.objects.filter(architecture_name=prodcut_name)
    if arch_info:
        for arch in arch_info:
            
            name=arch.architecture_name
            day_price=float("{0:.2f}".format(price_calculator(name)/30))
            month_price=price_calculator(name)
            year_price=float("{0:.2f}".format(price_calculator(name)*12))
            price=month_price
            image=arch.feature_img
        return render(request,"plans_wizard.html",{'name':name,'day_price':day_price,
            'month_price':month_price,"year_price":year_price,'image':image})
        
        print arch_info
    else:
        arch_info=Billing_Architecture.objects.filter(architecture_name=prodcut_name)
        for arch in arch_info:
            name=arch.architecture_name
            day_price=float("{0:.2f}".format(price_calculator(name)/30))
            month_price=price_calculator(name)
            year_price=float("{0:.2f}".format(price_calculator(name)*12))
            image=arch.architecture_img
            price=month_price
            print '**'*20
            print image
        return render(request,"plans_wizard.html",{'name':name,'price':price,'day_price':day_price,
            'month_price':month_price,"year_price":year_price,'image':image})

    #return HttpResponse("this is payements page")
def invoce_wizard(request):
    return render(request, 'invoice.html')

def dynamic_image_change(request):
    img_id=request.GET.get("img_id")
    #img_id="Sample Web Application"
    print "****"*20
    print "img id is :",img_id
    print "****"*20
    image_data={}
    main_arch_price=None
    price_dict={}
    try:
        img_val=int(img_id)
        #image_data=Billing_FeatureArchitecture.objects.filter(id=img_id)    
        fea_image=Billing_FeatureArchitecture.objects.filter(id=img_id)    
        
        for ftrd in fea_image:
            ftrd_dict={ftrd.id:[
            ftrd.architecture_name,
            price_calculator(ftrd.architecture_name),
            ftrd.feature_img,

            ]}
            price_dict.update(ftrd_dict)

        
        for k,v in price_dict.items():
            print '***'*20
            print k,
            print '***'*20
            print v

    except:
        imgname=""
        archname=ProductCode.objects.filter(value=img_id)
        image_data=Billing_Architecture.objects.filter(architecture_name=archname)
        for img in image_data:
            imgname=img.architecture_name
        main_arch_price=price_calculator(imgname)

        # for img in image_data:
        #     print img.architecture_name
        #     print img.architecture_img
        #     print img.price
    return render(request,"dynamic-side-img.html",{"image_data":image_data,
        'main_arch_price':main_arch_price,'price_dict':price_dict})

def invoice_info(request):
    uname=request.user.username
    email=request.user.email
    phone=userinfo.objects.get(user_id=request.user.id).phone
    uid=request.user.id
    invoice_num="%06d"%uid
    date=time.strftime("%d/%m/%Y")
    return render(request,"invoice_client_info.html",{"uname":uname,
        "phone":phone,"email":email,"invoice_num":invoice_num,"date":date})

def sendemail(request):
    ''' Sending Email'''
    success_message=""
    try:
        subject, from_email, to = 'So what are you waiting for?', 'vinod@ysec.io',['hareesh@ysec.io','hareeshkumar346@gmail.com','venkataramana@ysec.io','pruthvi@ysec.io']
        text_content = 'Please confirm your email address to activate your Cloud-TCO account.'
        html_content = render_to_string("promotional_mail.htm")
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        success_message = "mail sent"

    except:
        success_message = "mail failed"
    return HttpResponse("email status %s"%success_message)


# def view_that_asks_for_money(request):

#     # What you want the button to do.
#     paypal_dict = {
#         "business": "receiver_email@example.com",
#         "amount": "10.00",
#         "item_name": "name of the item",
#         "invoice": "unique-invoice-id",
#         "notify_url": "https://www.example.com" + reverse('paypal-ipn'),
#         "return_url": "https://www.example.com/your-return-location/",
#         "cancel_return": "https://www.example.com/your-cancel-location/",
#         "custom": "Upgrade all users!",  # Custom command to correlate to some function later (optional)
#     }

#     # Create the instance.
#     form = PayPalPaymentsForm(initial=paypal_dict)
#     context = {"form": form}
#     return render(request, "payment.html", context)



def billing_payment(request):
    custmr=Customer.objects.get(name=request.user.username)
    prvdr=Provider.objects.get(name="Cloud Providers")
    Payment(customer=custmr,provider=prvdr,amount=500,currency="US Dollar").save()
    return HttpResponse("this is tesitng")

def instance_launch(request):
    return render(request,"dashboard.html")

def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response   


def dashboard(request):
    return render(request,"profile-timeline.html")


def monitoring(request):
    userArch=UserArchitectures.objects.filter(username=request.user.username) 
    for ch in userArch:
        arcname=ch.arch_name
    print "***************"
    print arcname

    myArch=ProductCode.objects.filter(value=arcname)
    for sh in myArch:
        amd=sh.id
    print "*****************"
    print amd
    print "*****************"

    imgArch=Billing_Architecture.objects.filter(architecture_name_id=37)
    for ijk in imgArch:
        arc=ijk.architecture_img
    print "*****************"
    print arc
    print "*****************"
    return render(request,"profile-photos.html",{"userArch":userArch,"imgArch":imgArch})
 
import requests

def testingapi(request):
    Prdct_code=ProductCode.objects.filter(value="Model 2")
    plans_info=Plan.objects.get(name="daily plan")
    mtrd_id=None
    for pln in plans_info.metered_features.all():
        mtrd_id=pln.id
    print mtrd_id
    mtrd_info=MeteredFeature.objects.filter(id=mtrd_id)
    for mtrd in mtrd_info:
        print mtrd.unit
 
    return HttpResponse("hjghags")

def testwizard(request):
    return render(request,"test-wizard.htm")



def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response 


def sampletestview(request):
    return HttpResponse("this is sample test view")



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



''' 22/11/16 starting'''

def application(request):
    apptype=Billing_ArchitectureType.objects.filter(archtype="Application")
    app_image =  Billing_Architecture.objects.filter(archtype=apptype)   
    return render(request,"applications.html",{"apptype":apptype,"app":app_image})


def verticals(request):
    return render(request,"verticals.html")


''' 26/11/16 starting'''



# def rest_architecture(request):
#     token=Token.objects.get(user_id=request.user.id)
#     mytoken=token.key
#     arch_url="http://"+request.get_host()+reverse("architectures-list")
#     prdct_url="http://"+request.get_host()+reverse("productcode-list")
#     architectures=requests.get(arch_url, headers={'Authorization': 'Token {}'.format(mytoken)})
#     arch_json = architectures.json()
#     prdct_name=requests.get(prdct_url, headers={'Authorization': 'Token {}'.format(mytoken)})
#     prdct_json=prdct_name.json()
    
#     for prdct in prdct_json:
#         for arch in arch_json:
#             if prdct['id']==arch['architecture_name']:
#                 arch['architecture_name']=prdct['value']
#             else:
#                 pass
#     print arch_json
#     return HttpResponse(request.get_host())

def rest_main_architectures(request):
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    arch_url="http://"+request.get_host()+reverse("my-own-view")
    print '*** main architecture url'
    print arch_url

    architectures=requests.get(arch_url, headers={'Authorization': 'Token {}'.format(mytoken)})
    arch_json = architectures.json()
    return HttpResponse("arch comple te info")

def rest_arch_complete_info(request,pk):
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    
    arch_url="http://"+request.get_host()+reverse('ArchCompleInfo', kwargs={'pk':pk})
    
    print '*** architecture complete info url'
    print arch_url

    architectures=requests.get(arch_url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    arch_json = architectures.json()
    print arch_json
    return HttpResponse("this is testing")


def FtrdArchForArch(request,pk):
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    ftrd_arch_url="http://"+request.get_host()+reverse('FtrdArchByArchID', kwargs={'pk':pk})
    print '*** Featured architecture for a architecture by id url'
    print ftrd_arch_url



    ftrd_architectures=requests.get(ftrd_arch_url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    arch_json = ftrd_architectures.json()
    print arch_json
    return HttpResponse("this is testing")

def CompleteFtrdArchInfo(request,pk):
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    url="http://"+request.get_host()+reverse('FtrdArchCompleInfo', kwargs={'pk':pk})
    print '*** Featured architecture complete info url'
    print url
    info=requests.get(url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    arch_json = info.json()
    print arch_json
    return HttpResponse("this is testing")



def planspage(request,name):
    token=Token.objects.get(user_id=request.user.id)
    mytoken=token.key
    url="http://"+request.get_host()+reverse('PayPlansInfo', kwargs={'name':name})
    print "payment plans for a particular architectures url"
    print url

    info=requests.get(url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
    print '**'*20
    print info
    payplans = info.json()
    print '***'*20
    print payplans
    print '***'*20
    return HttpResponse("this is testing")


def invoicepage(request,name):
    return HttpResponse("this is invoice page demo")


# def complete_arch_info(request):
#     token=Token.objects.get(user_id=request.user.id)
#     mytoken=token.key
#     arch_url="http://"+request.get_host()+reverse('ArhitectureByID', kwargs={'pk':1})
#     architectures=requests.get(arch_url, headers={'Authorization': 'Token {}'.format(mytoken)}) 
#     arch_json = architectures.json()
#     prdct_url="http://"+request.get_host()+reverse('ProductCodeByID', kwargs={'pk':arch_json[0]['architecture_name']})
#     prdct_name=requests.get(prdct_url, headers={'Authorization': 'Token {}'.format(mytoken)})
#     prdct_json=prdct_name.json()
#     arch_json[0]['architecture_name']=prdct_json['value']
#     plan_url="http://"+request.get_host()+reverse('PlanByArchName', kwargs={'name':prdct_json['value']})
#     planinfo=requests.get(plan_url, headers={'Authorization': 'Token {}'.format(mytoken)})
#     data1 = arch_json[0]
#     data2 = planinfo.json()[0]
#     data1.update(data2)
#     print data1
#     return HttpResponse("dshjdsjdh")








# import requests
# mytoken = "4652400bd6c3df8eaa360d26560ab59c81e0a164"
# myurl = "http://localhost:8000/api/user_list"

# # A get request (json example):
# response = requests.get(myurl, headers={'Authorization': 'Token {}'.format(mytoken)})
# data = response.json()

