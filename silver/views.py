# Copyright (c) 2015 Presslabs SRL
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


from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from pyexcel_xls import get_data
import json

from silver.models import Proforma, Invoice
from silver.models.plans import MeteredFeature,RDS,S3Storage,LoadBalencer
from silver.models.product_codes import ProductCode
from tcoapp.models import Architecture,FeatureArchitecture
import csv


@login_required
def proforma_pdf(request, proforma_id):
    proforma = get_object_or_404(Proforma, id=proforma_id)
    return HttpResponseRedirect(proforma.pdf.url)


@login_required
def invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return HttpResponseRedirect(invoice.pdf.url)

import pyexcel as pe

def getxls(request):
    records = pe.iget_records(file_name="/home/ubuntu/Desktop/Python/01-11-16/cloudtco_updated/silver/mumbai-ec2-aws.xls")
    product_code=ProductCode.objects.get(value="EC2")
    return HttpResponse("this is text")
    
    # print "****"*20
    # print product_code
    # print "****"*20
    # #MeteredFeature.objects.all().delete()

    # for record in records:
    #   print "test"
    #   region=record["Location"]
    #   if region=="Asia Pacific (Mumbai)":
    #       print region
    #       try:
    #           MeteredFeature(termstype=record['TermType'],PriceDescription=record['PriceDescription'],
    #           EffectiveDate=record['EffectiveDate'],unit=record['Unit'],price_per_unit=record['PricePerUnit'],
    #           currency=record["Currency"],LeaseContractLength=record['LeaseContractLength'],PurchaseOption=record["PurchaseOption"],
    #           OfferingClass=record["OfferingClass"],Product_Family=record["Product Family"],serviceCode=record["serviceCode"],
    #           region=record["Location"],Location_Type=record["Location Type"],Instance_Type=record["Instance Type"],Current_Generation=record["Current Generation"],
    #           Instance_Family=record["Instance Family"],vCPU=record["vCPU"],Physical_Processor=record["Physical Processor"],
    #           Clock_Speed=record["Clock Speed"],Memory=record["Memory"],Storage=record["Storage"],Network_Performance=record["Network Performance"],Processor_Architecture=record["Processor Architecture"],
    #           Storage_Media=record["Storage Media"],Volume_Type=record["Volume Type"],Max_Volume_Size=record["Max Volume Size"],Max_IOPS_volume=record["Max IOPS/volume"],Max_IOPS_Burst_Performance=record["Max IOPS Burst Performance"],
    #           Max_throughput_volume=record["Max throughput/volume"],Provisioned=record["Provisioned"],Tenancy=record["Tenancy"],EBS_Optimized=record["EBS Optimized"],
    #           ostype=record["Operating System"],License_Model=record["License Model"],Group=record["Group"],
    #           Group_Description=record["Group Description"],Transfer_Type=record["Transfer Type"],From_Location=record["From Location"],From_Location_Type=record["From Location Type"],
    #           To_Location=record["To Location"],To_Location_Type=record["To Location Type"],usageType=record["usageType"],
    #           operation=record["operation"],Dedicated_EBS_Throughput=record["Dedicated EBS Throughput"],Enhanced_Networking_Supported=record["Enhanced Networking Supported"],GPU=record["GPU"],Instance_Capacity_10xlarge=record["Instance Capacity - 10xlarge"],Instance_Capacity_2xlarge=record["Instance Capacity - 2xlarge"],Instance_Capacity_4xlarge=record["Instance Capacity - 4xlarge"],Instance_Capacity_8xlarge=record["Instance Capacity - 8xlarge"],Instance_Capacity_large=record["Instance Capacity - large"],Instance_Capacity_medium=record["Instance Capacity - medium"],
    #           Instance_Capacity_xlarge=record["Instance Capacity - xlarge"],Intel_AVX_Available=record["Intel AVX Available"],Intel_AVX2_Available=record["Intel AVX2 Available"],Intel_Turbo_Available=record["Intel Turbo Available"],Physical_Cores=record["Physical Cores"],Pre_Installed_SW=record["Pre Installed S/W"],Processor_Features=record["Processor Features"],included_units=1,
    #           name=record["Instance Type"],product_code=product_code,
    #           ).save()
    #       except:
    #           pass
    #   else:
    #       pass
    
        # MeteredFeature(termstype=record['TermType'],PriceDescription=record['PriceDescription'],
        #   record['EffectiveDate']
        #   ).save()
        
    # workbook = xlrd.open_workbook("/home/ubuntu/Desktop/Python/01-11-16/cloudtco_updated/silver/mumbai-ec2-aws.xls")
    # worksheet = workbook.sheet_by_name('ec2')
    # print worksheet.cell(0, 1).value

    # print "***"*20
    # data = get_data("/home/ubuntu/Desktop/Python/01-11-16/cloudtco_updated/silver/mumbai-ec2-aws.xls")
    # json_data=json.dumps(data)
    # meterd_data_json=json.loads(json_data)
    # #meterd_data=meterd_data_json['Sheet1'][:1]
    # print '**'*20
    # print meterd_data_json
    # print '**'*20
    # product_code=ProductCode.objects.get(value="Sample instance")
    
    # #print product_code
    # # for mtr in meterd_data:
    # #     print mtr[0]
    # #     print mtr[1]
    # #     MeteredFeature(region=mtr[0],ostype=mtr[2],name=mtr[1],unit="vcpu",
    # #         price_per_unit=mtr[7],included_units=mtr[3],product_code=product_code).save()
    
    

def store_data(request):
    architecture=Architecture.objects.all()
    ftrd_arch=FeatureArchitecture.objects.all()
    for archname in architecture:
        try:
            ProductCode(value=archname.architecture_name).save()
        except:
            pass
    for ftrdname in ftrd_arch:
        try:
            ProductCode(value=ftrdname.architecture_name).save()
        except:
            pass
    return HttpResponse("this is test")

def csv_data(request):
    product_code=ProductCode.objects.get(value="EC2")
    #MeteredFeature.objects.all().delete()
    with open('/home/ubuntu/Desktop/Python/11-11-16/cloudtco_updated/silver/loadbalancer.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0]=="OnDemand" and row[11]=="Asia Pacific (Mumbai)":
                LoadBalencer(termstype=row[0],PriceDescription=row[1],
                          EffectiveDate=row[2],unit=row[3],price_per_unit=row[4],
                          currency=row[5],LeaseContractLength=row[6],PurchaseOption=row[7],
                          OfferingClass=row[8],Product_Family=row[9],serviceCode=row[10],
                          region=row[11],Location_Type=row[12],Instance_Type=row[13],Current_Generation=row[14],
                          Instance_Family=row[15],vCPU=row[16],Physical_Processor=row[17],
                          Clock_Speed=row[18],Memory=row[19],Storage=row[20],Network_Performance=row[21],Processor_Architecture=row[22],
                          Storage_Media=row[23],Volume_Type=row[24],Max_Volume_Size=row[25],Max_IOPS_volume=row[26],Max_IOPS_Burst_Performance=row[27],
                          Max_throughput_volume=row[28],Provisioned=row[29],Tenancy=row[30],EBS_Optimized=row[31],
                          ostype=row[32],License_Model=row[33],Group=row[34],
                          Group_Description=row[35],Transfer_Type=row[36],From_Location=row[37],From_Location_Type=row[38],
                          To_Location=row[39],To_Location_Type=row[40],usageType=row[41],
                          operation=row[42],Dedicated_EBS_Throughput=row[43],Enhanced_Networking_Supported=row[44],GPU=row[45],Instance_Capacity_10xlarge=row[46],Instance_Capacity_2xlarge=row[47],Instance_Capacity_4xlarge=row[48],Instance_Capacity_8xlarge=row[49],Instance_Capacity_large=row[50],Instance_Capacity_medium=row[51],
                          Instance_Capacity_xlarge=row[52],Intel_AVX_Available=row[53],Intel_AVX2_Available=row[54],Intel_Turbo_Available=row[55],Physical_Cores=row[56],Pre_Installed_SW=row[57],Processor_Features=row[58],included_units=1,
                          name=row[13],product_code=product_code
                          ).save()               
            else:
                pass
    #print len(mumbai_list)
    return HttpResponse("this is csv import")


def rds_data(request):
    with open('/home/ubuntu/Desktop/Python/09-11-16/cloudtco_updated/silver/rds.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            print row
            if row[0]=="OnDemand" and row[14]=="Asia Pacific (Mumbai)":
                print "data store"
                RDS(termstype=row[0],PriceDescription=row[1],EffectiveDate=row[2],StartingRange=row[3],EndingRange=row[4],unit=row[5],price_per_unit=row[6],
                          currency=row[7],RelatedTo=row[8],LeaseContractLength=row[9],PurchaseOption=row[10],
                          OfferingClass=row[11],Product_Family=row[12],serviceCode=row[13],
                          region=row[14],Location_Type=row[15],Instance_Type=row[16],Current_Generation=row[17],
                          Instance_Family=row[18],vCPU=row[19],Physical_Processor=row[20],
                          Clock_Speed=row[21],Memory=row[22],Storage=row[23],Network_Performance=row[24],Processor_Architecture=row[25],
                         engine_code=row[26],Database_Engine=row[27],Database_Edition=row[28],
                        License_Model=row[29],Deployment_Option=row[30],Transfer_Type=row[31],From_Location=row[32],From_Location_Type=row[33],
                            To_Location=row[34],To_Location_Type=row[35],usageType=row[36],operation=row[37],Dedicated_EBS_Throughput=row[38],
                            Enhanced_Networking_Supported=row[39],Processor_Features=[40]
                          ).save()               
            else:
                print "failed"
                pass
    #print len(mumbai_list)
    return HttpResponse("this is rds import")

def s3storage(request):
    with open('/home/ubuntu/Desktop/Python/09-11-16/cloudtco_updated/silver/s3.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[13]=="Asia Pacific (Mumbai)":
                print "data store"
                S3Storage(SKU=row[0],OfferTermCode=row[1],RateCode=row[2],termstype=row[3],PriceDescription=row[4],EffectiveDate=row[5],StartingRange=row[6],
                          EndingRange=row[7],Unit=row[8],price_per_unit=row[9],currency=row[10],
                          Product_Family=row[11],serviceCode=row[12],region=row[13],
                          Location_Type=row[14],Availability=row[15],Storage_class=row[16],Volume_Type=row[17],
                          Fee_Code=row[18],Fee_Description=row[19],Group=row[20],
                          Group_Description=row[21],Transfer_Type=row[22],From_Location=row[23],From_Location_Type=row[24],
                            To_Location=row[25],To_Location_Type=row[26],
                         usageType=row[27],operation=row[28],Durability=row[29]
                          ).save()               
            else:
                print "failed"
                pass
    return HttpResponse("this is s3storage")

def ses_storage(request):
    with open('/home/ubuntu/Desktop/Python/09-11-16/cloudtco_updated/silver/s3.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[13]=="Asia Pacific (Mumbai)":
                print "data store"
                S3Storage(SKU=row[0],OfferTermCode=row[1],RateCode=row[2],termstype=row[3],PriceDescription=row[4],EffectiveDate=row[5],StartingRange=row[6],
                          EndingRange=row[7],Unit=row[8],price_per_unit=row[9],currency=row[10],
                          Product_Family=row[11],serviceCode=row[12],region=row[13],
                          Location_Type=row[14],Availability=row[15],Storage_class=row[16],Volume_Type=row[17],
                          Fee_Code=row[18],Fee_Description=row[19],Group=row[20],
                          Group_Description=row[21],Transfer_Type=row[22],From_Location=row[23],From_Location_Type=row[24],
                            To_Location=row[25],To_Location_Type=row[26],
                         usageType=row[27],operation=row[28],Durability=row[29]
                          ).save()               
            else:
                print "failed"
                pass
    return HttpResponse("this is s3storage")

