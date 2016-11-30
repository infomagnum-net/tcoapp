# Copyright (c) 2016 Presslabs SRL
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.db import models


class ProductCode(models.Model):
    value = models.CharField(max_length=128, unique=True)
    def __unicode__(self):
        return unicode(self.value)


class Billing_ArchitectureType(models.Model):
    archtype = models.CharField(max_length=15,blank=True,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return unicode(self.archtype)


class Billing_Architecture(models.Model):
    architecture_name = models.ForeignKey(ProductCode)
    architecture_img = models.ImageField(upload_to = 'architectures',null=True, blank=True)
    archtype = models.ForeignKey(Billing_ArchitectureType,blank=True,null=True)
    description = models.TextField(blank=True)
    def __unicode__(self):
        #return '%d: %s,%s' % (self.id,self.architecture_name, self.architecture_img)
        return unicode(self.id)


class Billing_FeatureArchitecture(models.Model):
    architecture_id = models.ForeignKey(Billing_Architecture)
    feature_img = models.ImageField(upload_to = 'architectures/features/',null=True, blank=True)
    architecture_name = models.ForeignKey(ProductCode)
    description = models.TextField(blank=True)

