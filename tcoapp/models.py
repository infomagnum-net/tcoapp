from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class ArchitectureType(models.Model):
    archtype = models.CharField(max_length=15,blank=True,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __unicode__(self): return u"%s" % self.archtype

class Chat(models.Model):
    user_id = models.IntegerField(null=True)
    usermsg = models.TextField(blank=True,null=True)
    botmsg=models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

class userinfo(models.Model):
    user_id = models.IntegerField()
    phone = models.CharField(max_length=15)
    reg_cnrrm_code=models.CharField(max_length=250,blank=True,null=True)
    iam_access_key = models.CharField(max_length=100, blank=True)
    iam_secret_key = models.CharField(max_length=100, blank=True)
    iam_status = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_img = models.ImageField(upload_to = 'profile',null=True, blank=True)

class Architecture(models.Model):
    architecture_name = models.CharField(max_length=100,unique=True)
    architecture_img = models.ImageField(upload_to = 'architectures',null=True, blank=True)
    price = models.FloatField(null=True, blank=True, default=None)
    archtype = models.ForeignKey(ArchitectureType,blank=True,null=True)

    # def __str__(self):
    #     return self.architecture_img
    def __unicode__(self): return u"%s" % self.id

class FeatureArchitecture(models.Model):
    architecture_id = models.ForeignKey(Architecture)
    feature_img = models.ImageField(upload_to = 'architectures/features/',null=True, blank=True)
    architecture_name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, blank=True)
    price = models.FloatField(null=True, blank=True, default=None)
    
class CreditUser(models.Model):      
    user_id = models.IntegerField()
    stripe_id = models.IntegerField()
    plan_type = models.CharField(max_length=100, blank=True)
    card_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

