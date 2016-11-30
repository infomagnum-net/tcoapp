import boto3
import logging
import subprocess

LOG = logging.getLogger(__name__)

# from django.conf import settings.AWS_ACCESS_KEY
# from django.conf import settings.AWS_SECRET_KEY

AWS_ACCESS_KEY = 'AKIAII45QZAB34UTPY6Q'
AWS_SECRET_KEY = '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'
region_name='ap-northeast-1'

# boto3.set_stream_logger('botocore', level='DEBUG')
class AWSAdmin(object):
    def __init__(self):
        self.iam_con = boto3.client('iam', region_name=region_name, aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)        
        self.cloud = boto3.client('cloudformation', region_name=region_name)    
        self.ec2_con = boto3.client('ec2', region_name=region_name)
        self.autoscale_con = boto3.client('autoscaling', region_name=region_name)
        self.elb_con = boto3.client('elb', region_name=region_name)
        self.rds_con = boto3.client('rds', region_name=region_name)
        self.opsworks_con = boto3.client('opsworks', region_name=region_name)
        self.elasticbeanstalk_con = boto3.client('elasticbeanstalk', region_name=region_name)
        self.s3_con = boto3.client('s3', region_name=region_name)        


    def create_IAM(self, user_name, user_path):
        iam = self.iam_con
        response = iam.create_user(
            Path=user_path,
            UserName=user_name
        )
        return response
    def create_IAM_KEY(self, user_name):
        iam = self.iam_con
        response = iam.create_access_key(
            UserName=user_name
        )
        return response

    def create_vpc(self, cidr):
        ec2 = self.ec2_con
        response = ec2.create_vpc(
            # DryRun=True|False,
            CidrBlock=cidr,
            InstanceTenancy='default'
        )
        return response

    def create_subnet(self, sub_zone, sub_cidr, vpc_id):
        ec2 = self.ec2_con
        response = ec2.create_subnet(
            # DryRun=True|False,
            VpcId=vpc_id,
            CidrBlock=sub_cidr,
            AvailabilityZone=sub_zone
        )
        return response

    def create_routeTable(self, vpc_id):
        ec2 = self.ec2_con        
        response = ec2.create_route_table(
            # DryRun=True|False,
            VpcId=vpc_id
        )
        return response
    def assign_routeTable(self, subnet_id, rTable_id):
        ec2 = self.ec2_con
        response = ec2.associate_route_table(
            # DryRun=True|False,
            SubnetId=subnet_id,
            RouteTableId=rTable_id
        )
        return response

    def create_SecurityGroup(self, sg_name, sg_desc, vpc_id):
        ec2 = self.ec2_con        
        response = ec2.create_security_group(
            # DryRun=True|False,
            GroupName=sg_name,
            Description=sg_desc,
            VpcId=vpc_id
        )
        return response

    def create_IGW(self):
        ec2 = self.ec2_con        
        response = ec2.create_internet_gateway()
        return response

    def attach_IGW(self, ):
        ec2 = self.ec2_con
        response  = attach_internet_gateway(
            # DryRun=True|False,
            InternetGatewayId='string',
            VpcId='string'
        )
        return response

    def create_nat(self):
        ec2 = self.ec2_con        
        response = ec2.create_internet_gateway()
        return response
        # pass
        
    def elastic_Ip_address(self):
        ec2 = self.ec2_con        
        response = ec2.allocate_address()
        return response

    def authorize_sg(self, sg_id):
        ''' Security group authorization'''
        ec2 = self.ec2_con 
        response = ec2.authorize_security_group_ingress(
            # DryRun=True|False,
            # GroupName='string',
            GroupId=sg_id,
            # SourceSecurityGroupName='string',
            # SourceSecurityGroupOwnerId='string',
            IpProtocol='string',
            FromPort=123,
            ToPort=123,
            CidrIp='string',
            IpPermissions=[
                {
                    'IpProtocol': 'string',
                    'FromPort': 123,
                    'ToPort': 123,
                    'UserIdGroupPairs': [
                        {
                            'UserId': 'string',
                            'GroupName': 'string',
                            'GroupId': 'string',
                            'VpcId': 'string',
                            'VpcPeeringConnectionId': 'string',
                            'PeeringStatus': 'string'
                        },
                    ],
                    'IpRanges': [
                        {
                            'CidrIp': 'string'
                        },
                    ],
                    'PrefixListIds': [
                        {
                            'PrefixListId': 'string'
                        },
                    ]
                },
            ]
        )

        return response


    def cf_estimate(self, template_url, param_key):
        print "estimation"        
        cf = self.cloud
        response = cf.estimate_template_cost(
            # TemplateBody='string',
            TemplateURL= template_url,
            Parameters=[
                {
                    'ParameterKey': param_key,
                    'ParameterValue': '',
                    'UsePreviousValue': True
                },
            ]
        )
        return response

    def cf_create_stack(self, stack_name, template_url, key_name, stack_policy, key_tag, val_tag):
        ''' Creating a stack for cloud formation '''
        cf = self.cloud
        response = cf.create_stack(
            StackName=stack_name,
            # TemplateBody='string',
            TemplateURL=template_url,
            Parameters=[
                {
                    'ParameterKey': key_name,
                    'ParameterValue': '',
                    'UsePreviousValue': True
                },
            ],
            DisableRollback=False,
            TimeoutInMinutes=123,
            # NotificationARNs=[
            #     'string',
            # ],
            # Capabilities=[
            #     'CAPABILITY_IAM'|'CAPABILITY_NAMED_IAM',
            # ],
            ResourceTypes=[
                'string',
            ],
            # RoleARN='string',
            OnFailure='ROLLBACK',
            # StackPolicyBody='string',
            StackPolicyURL=stack_policy,
            Tags=[
                {
                    'Key': key_tag,
                    'Value': val_tag
                },
            ]
        )
        return response

    def cf_update_stack(self, stack_name, template_url, key_name, stack_policy, key_tag, val_tag):
        ''' Updating a stack for cloud formation '''
        cf = self.cloud
        response = cf.update_stack(
            StackName=stack_name,
            # TemplateBody='string',
            TemplateURL=template_url,
            Parameters=[
                {
                    'ParameterKey': key_name,
                    'ParameterValue': '',
                    'UsePreviousValue': True
                },
            ],
            DisableRollback=False,
            TimeoutInMinutes=123,
            # NotificationARNs=[
            #     'string',
            # ],
            # Capabilities=[
            #     'CAPABILITY_IAM'|'CAPABILITY_NAMED_IAM',
            # ],
            ResourceTypes=[
                'string',
            ],
            # RoleARN='string',
            OnFailure='ROLLBACK',
            # StackPolicyBody='string',
            StackPolicyURL=stack_policy,
            Tags=[
                {
                    'Key': key_tag,
                    'Value': val_tag
                },
            ]
        )
        return response


    def create_instance(self, ami_id, keyname, inst_type, aval_zone, subnet_id, security_group):
        """ Creating Ec2 Instance """

        ec2 = self.ec2_con
        # if True:
        #     pass
        # else:
        #     pass
        response = ec2.run_instances(
            # DryRun=True|False,
            ImageId=ami_id,
            MinCount=1,
            MaxCount=1,
            KeyName=keyname,
            # SecurityGroups=[
            #     'string',
            # ],
            # SecurityGroupIds=[
            #     security_group,
            # ],
            UserData='string',
            InstanceType=inst_type,
            Placement={
                'AvailabilityZone': aval_zone,
                # 'GroupName': 'string',
                # 'Tenancy': 'default'|'dedicated'|'host',
                # 'HostId': 'string',
                # 'Affinity': 'string'
            },
            # KernelId='string',
            # RamdiskId='string',
            BlockDeviceMappings=[
                {
                    # 'VirtualName': 'string',
                    'DeviceName': '/dev/sdb',
                    'Ebs': {
                        # 'SnapshotId': 'string',
                        'VolumeSize': 8,
                        'DeleteOnTermination': True,
                        'VolumeType': 'gp2',
                        # 'Iops': 123,
                        'Encrypted': False
                    },
                    # 'NoDevice': 'string'
                },
            ],
            Monitoring={
                'Enabled': False
            },
            # SubnetId=subnet_id,
            # DisableApiTermination=True|False,
            InstanceInitiatedShutdownBehavior='stop',
            # PrivateIpAddress='string',
            # ClientToken='string',
            # AdditionalInfo='string',
            NetworkInterfaces=[
                {
                    # 'NetworkInterfaceId': 'string',
                    'DeviceIndex': 0,
                    'SubnetId': subnet_id,
                    # 'Description': 'string',
                    # 'PrivateIpAddress': 'string',
                    'Groups': [
                        security_group,
                    ],
                    # 'DeleteOnTermination': True|False,
                    # 'PrivateIpAddresses': [
                    #     {
                    #         'PrivateIpAddress': 'string',
                    #         'Primary': True|False
                    #     },
                    # ],
                    # 'SecondaryPrivateIpAddressCount': 123,
                    'AssociatePublicIpAddress': True
                },
            ],
            # IamInstanceProfile={
            #     'Arn': 'string',
            #     'Name': 'string'
            # },
            EbsOptimized=False
        )
        return response

    def terminate_instance(self, inst_id):

        ec2 = self.ec2_con
        response = ec2.terminate_instances(
            # DryRun=True|False,
            InstanceIds=[
                inst_id,
            ]
        )
        return response

    def stop_instance(self, inst_id):

        ec2 = self.ec2_con
        response = ec2.stop_instances(
            # DryRun=True|False,
            InstanceIds=[
                inst_id,
            ],
            Force=False
        )
        return response

    def create_launch_configuration(self, lconfig_name, image_id, key_name, sg_id, inst_id, inst_type,
        vol_size):
        ''' Launch Configuration'''
        autoscale = self.autoscale_con
        response = autoscale.create_launch_configuration(
            LaunchConfigurationName=lconfig_name,
            ImageId=image_id,
            KeyName=key_name,
            SecurityGroups=[
                sg_id,
            ],
            # ClassicLinkVPCId='string',
            # ClassicLinkVPCSecurityGroups=[
            #     'string',
            # ],
            # UserData='string',
            InstanceId=inst_id,
            InstanceType=inst_type,
            # KernelId='string',
            # RamdiskId='string',
            BlockDeviceMappings=[
                {
                    # 'VirtualName': 'string',
                    'DeviceName': '/dev/xvda', #/dev/sdh
                    'Ebs': {
                        # 'SnapshotId': 'string',
                        'VolumeSize': vol_size,
                        'VolumeType': 'gp2',
                        'DeleteOnTermination': True,
                        # 'Iops': 123,
                        'Encrypted': False
                    },
                    # 'NoDevice': True|False
                },
            ],
            InstanceMonitoring={
                'Enabled': False
            },
            # SpotPrice='string',
            # IamInstanceProfile='string',
            EbsOptimized=False,
            AssociatePublicIpAddress=True,
            # PlacementTenancy='string'
            )
        return response

    def asg_create(self, asg_name, lconfig_name, min_size, max_size, desired_capacity, default_cool,
        aval_zone, load_bal_name, key_name, key_val):
        ''' Autoscaling group creation '''
        print "ASG creation"
        asg = self.autoscale_con
        response = asg.create_auto_scaling_group(
            AutoScalingGroupName=asg_name,
            LaunchConfigurationName=lconfig_name,
            # InstanceId=inst_id,
            MinSize=min_size,
            MaxSize=max_size,
            DesiredCapacity=desired_capacity, #Ec2 instances size
            DefaultCooldown=default_cool, #300 seconds
            AvailabilityZones=[
                aval_zone,
            ],
            LoadBalancerNames=[
                load_bal_name,
            ],
            # TargetGroupARNs=[
            #     'string',
            # ],
            HealthCheckType='ELB',
            HealthCheckGracePeriod=0,
            # PlacementGroup='string',
            # VPCZoneIdentifier='string',
            # TerminationPolicies=[
            #     'string',
            # ],
            NewInstancesProtectedFromScaleIn=False,
            Tags=[
                {
                    # 'ResourceId': 'string',
                    # 'ResourceType': 'string',
                    'Key': key_name,
                    'Value': key_val,
                    'PropagateAtLaunch': False
                },
            ]
            )

        return response  

    def asg_update(self, asg_name, lconfig_name, min_size, max_size, desired_capacity, default_cool,
        aval_zone, load_bal_name, key_name, key_val):
        ''' Autoscaling group updation '''
        
        asg = self.autoscale_con
        response = asg.create_auto_scaling_group(
            AutoScalingGroupName=asg_name,
            LaunchConfigurationName=lconfig_name,
            # InstanceId=inst_id,
            MinSize=min_size,
            MaxSize=max_size,
            DesiredCapacity=desired_capacity, #Ec2 instances size
            DefaultCooldown=default_cool, #300 seconds
            AvailabilityZones=[
                aval_zone,
            ],
            LoadBalancerNames=[
                load_bal_name,
            ],
            # TargetGroupARNs=[
            #     'string',
            # ],
            HealthCheckType='ELB',
            HealthCheckGracePeriod=0,
            # PlacementGroup='string',
            # VPCZoneIdentifier='string',
            # TerminationPolicies=[
            #     'string',
            # ],
            NewInstancesProtectedFromScaleIn=False,
            Tags=[
                {
                    # 'ResourceId': 'string',
                    # 'ResourceType': 'string',
                    'Key': key_name,
                    'Value': key_val,
                    'PropagateAtLaunch': False
                },
            ]
            )

        return response

    def terminate_asg_instance(self, inst_id):

        asg = self.autoscale_con
        response = asg.terminate_instance_in_auto_scaling_group(
            InstanceId=inst_id,
            ShouldDecrementDesiredCapacity=True # automatically decrease the autoscaling group size
        )
        return response
    def complete_lifecycle(self, asg_name):

        asg = self.autoscale_con
        response = asg.describe_auto_scaling_groups(
            AutoScalingGroupNames=[
                asg_name,
            ],
            # NextToken='string',
            MaxRecords=123
        )
        # response = client.describe_scaling_policies(
        #     PolicyNames=[
        #         'string',
        #     ],
        #     ServiceNamespace='ec2',
        #     ResourceId='string',
        #     ScalableDimension='ecs:service:DesiredCount'|'ec2:spot-fleet-request:TargetCapacity',
        #     MaxResults=123,
        #     NextToken='string'
        # )


        # response = asg.describe_auto_scaling_groups(
        #     AutoScalingGroupNames=[
        #         asg_name,
        #     ],
        #     NextToken='string',
        #     MaxRecords=123
        # ) 

        return response 

    def ath_load_bal(self, asg_name, load_bal_name):
        ''' Attaching Load Balancers to Autoscaling group'''
        asg = self.autoscale_con
        response = asg.attach_load_balancers(
            AutoScalingGroupName=asg_name,
            LoadBalancerNames=[
                load_bal_name,
            ]
        )
        return response

    def create_load_balancer(self, load_bal_name, protocol, load_bal_port, aval_zone, subnet_id, sg_id,
        key_name, key_value):
        ''' Creating Load Balancer '''
        loadbal_client = self.elb_con
        response = loadbal_client.create_load_balancer(
            LoadBalancerName=load_bal_name,
            Listeners=[
                {
                    'Protocol': protocol,
                    'LoadBalancerPort': load_bal_port, # 80, 443
                    'InstanceProtocol': 'http',
                    'InstancePort': load_bal_port, #the port on which instance is listening
                    # 'SSLCertificateId': 'string' # ARN name
                },
            ],
            AvailabilityZones=[
                aval_zone,
            ],
            Subnets=[
                subnet_id,
            ],
            SecurityGroups=[
                sg_id,
            ],
            Scheme='string',
            Tags=[
                {
                    'Key': key_name,
                    'Value': key_value
                },
            ]
        )

        return response

    def add_load_balancer(self):
        autoscale = self.autoscale_con            
        response = autoscale.attach_load_balancers()
        return response

    def create_elb():
        elb = self.elb_con
        response = elb.create_load_balancer()
        return response

    def bean_create_application(self, app_name, desc):
        beanstalk_con = self.elasticbeanstalk_con
        response = beanstalk_con.create_application(
            ApplicationName=app_name,
            Description=desc
        )
        return response

    def bean_delete_application(self, app_name):
        beanstalk_con = self.elasticbeanstalk_con
        response = beanstalk_con.delete_application(
            ApplicationName=app_name,
            TerminateEnvByForce=False
        )
        return response

    def bean_update_application(self, app_name, desc):
        beanstalk_con = self.elasticbeanstalk_con
        response = beanstalk_con.update_application(
            ApplicationName=app_name,
            Description=desc
        )
        return response

    def bean_create_env(self, app_name, env_name, group_name, description, cname_prefix, tier_name, tier_type,
        tier_version, tags_key, tags_val, version_label, template_name, solution_stack_name, option_settings_resource_name,
        option_settings_name_space, option_settings_option_name, option_settings_value, 
        options_to_remove_resource_name, options_to_remove_name_space, options_to_remove_option_name):

        beanstalk_con = self.elasticbeanstalk_con
        response = beanstalk_con.create_environment(
            ApplicationName=app_name,
            EnvironmentName=env_name,
            GroupName=group_name,
            Description=description,
            CNAMEPrefix=cname_prefix,
            Tier={
                'Name': tier_name,
                'Type': tier_type,
                'Version': tier_version
            },
            Tags=[
                {
                    'Key': tags_key,
                    'Value': tags_val
                },
            ],
            VersionLabel=version_label,
            TemplateName=template_name,
            SolutionStackName=solution_stack_name,
            OptionSettings=[
                {
                    'ResourceName': option_settings_resource_name,
                    'Namespace': option_settings_name_space,
                    'OptionName': option_settings_option_name,
                    'Value': option_settings_value
                },
            ],
            OptionsToRemove=[
                {
                    'ResourceName': options_to_remove_resource_name,
                    'Namespace': options_to_remove_name_space,
                    'OptionName': options_to_remove_option_name
                },
            ]
        )
        return response

    def bean_del_env(self, app_name, env_name):

        beanstalk_con = self.elasticbeanstalk_con
        response = beanstalk_con.delete_environment_configuration(
            ApplicationName=app_name,
            EnvironmentName=env_name
        )
        return response

    def bean_update_env(self, app_name, env_id, env_name, group_name, desc, tier_name, tier_type,
        tier_version, version_label, template_name, solution_stack_name, option_settings_resource_name,
        option_settings_name_space, option_settings_option_name, option_settings_value, options_to_remove_resource_name,
        options_to_remove_name_space, options_to_remove_option_name):

        beanstalk_con = self.elasticbeanstalk_con
        response = beanstalk_con.update_environment(
            ApplicationName=app_name,
            EnvironmentId=env_id,
            EnvironmentName=env_name,
            GroupName=group_name,
            Description=desc,
            Tier={
                'Name': tier_name,
                'Type': tier_type,
                'Version': tier_version
            },
            VersionLabel=version_label,
            TemplateName=template_name,
            SolutionStackName=solution_stack_name,
            OptionSettings=[
                {
                    'ResourceName': option_settings_resource_name,
                    'Namespace': option_settings_name_space,
                    'OptionName': option_settings_option_name,
                    'Value': option_settings_value
                },
            ],
            OptionsToRemove=[
                {
                    'ResourceName': options_to_remove_resource_name,
                    'Namespace': options_to_remove_name_space,
                    'OptionName': options_to_remove_option_name
                },
            ]
        )
        return response

    def bean_create_config_template(self, app_name, template_name, solution_stack_name,
        source_config_app_name, source_config_template_name, env_id, desc, option_settings_resource_name, option_settings_name_space,
        option_settings_option_name, option_settings_value):

        beanstalk_con = self.elasticbeanstalk_con
        response = beanstalk_con.create_configuration_template(
            ApplicationName=app_name,
            TemplateName=template_name,
            SolutionStackName=solution_stack_name,
            SourceConfiguration={
                'ApplicationName': source_config_app_name,
                'TemplateName': source_config_template_name
            },
            EnvironmentId=env_id,
            Description=desc,
            OptionSettings=[
                {
                    'ResourceName': option_settings_resource_name,
                    'Namespace': option_settings_name_space,
                    'OptionName': option_settings_option_name,
                    'Value': option_settings_value
                },
            ]
        )
        return response

    def bean_del_config_template(self, app_name, template_name):

        beanstalk_con = self.elasticbeanstalk_con
        response = beanstalk_con.delete_configuration_template(
            ApplicationName=app_name,
            TemplateName=template_name
        )
        return response

    def bean_update_config_template(self, app_name, template_name, desc, option_settings_resource_name,
        option_settings_name_space, option_settings_option_name, option_settings_value):

        beanstalk_con = self.elasticbeanstalk_con
        response = beanstalk_con.update_configuration_template(
            ApplicationName=app_name,
            TemplateName=template_name,
            Description=desc,
            OptionSettings=[
                {
                    'ResourceName': option_settings_resource_name,
                    'Namespace': option_settings_name_space,
                    'OptionName': option_settings_option_name,
                    'Value': option_settings_value
                },
            ],
            # OptionsToRemove=[
            #     {
            #         'ResourceName': 'string',
            #         'Namespace': 'string',
            #         'OptionName': 'string'
            #     },
            # ]
        )
        return response


    def s3_create_bucket(self, bucket_name, bucket_config):        
        s3 = self.s3_con
        response = s3.create_bucket(
            # ACL='private'|'public-read'|'public-read-write'|'authenticated-read',
            Bucket=bucket_name,
            CreateBucketConfiguration={
                bucket_config
            },
            # GrantFullControl='string',
            # GrantRead='string',
            # GrantReadACP='string',
            # GrantWrite='string',
            # GrantWriteACP='string'
        )
        return response
    def s3_delete_bucket(self, bucket_name):        
        s3 = self.s3_con
        response = s3.delete_bucket(            
            Bucket=bucket_name            
        )
        return response

    def create_multi_part(self):
        s3 = self.s3_con        
        response = s3.create_multipart_upload(
            ACL='private'|'public-read'|'public-read-write'|'authenticated-read'|'aws-exec-read'|'bucket-owner-read'|'bucket-owner-full-control',
            Bucket='string',
            CacheControl='string',
            ContentDisposition='string',
            ContentEncoding='string',
            ContentLanguage='string',
            ContentType='string',
            Expires=datetime(2015, 1, 1),
            GrantFullControl='string',
            GrantRead='string',
            GrantReadACP='string',
            GrantWriteACP='string',
            Key='string',
            Metadata={
                'string': 'string'
            },
            ServerSideEncryption='AES256'|'aws:kms',
            StorageClass='STANDARD'|'REDUCED_REDUNDANCY'|'STANDARD_IA',
            WebsiteRedirectLocation='string',
            SSECustomerAlgorithm='string',
            SSECustomerKey='string',
            SSEKMSKeyId='string',
            RequestPayer='requester'
        )
        return response

    def user_data(self):
        script1 = """ 
        #!/bin/bash
        yum update
        yum install httpd php php-mysql stress -y
        cd /etc/httpd/conf
        cp httpd.conf httpdconfbackup.conf
        rm -rf httpd.conf
        wget https://s3-eu-west-1.amazonaws.com/acloudguru/config/httpd.conf
        cd /var/www/html
        echo "healthy" > healthy.html
        wget https://wordpress.org/latest.tar.gz
        tar -xzf latest.tar.gz
        cp -r wordpress/* /var/www/html/
        rm -rf wordpress
        rm -rf latest.tar.gz
        chmod -R 755 wp-content
        chown -R apache.apache wp-content
        service httpd start
        chkconfig httpd on
        """
        print "user data script"
        # with open 
        # with open('./bashscript.sh', 'rb') as file:
        # script1 = file.read()
        # rc = call(script)
        return script1

    def rds_sg(self, rds_sg_name, rds_sg_desc, rds_sg_key, rds_sg_val):

        RDS = self.rds_con
        response = RDS.create_db_security_group(
            DBSecurityGroupName=rds_sg_name,
            DBSecurityGroupDescription=rds_sg_desc,
            Tags=[
                {
                    'Key': rds_sg_key,
                    'Value': rds_sg_val
                },
            ]
        )

        return response

    def rds_instance(self, rds_db, rds_dbinstance, rds_dbstore, rds_dbinst, rds_dbengine, rds_dbuser,
        rds_dbpwd, rds_sg, rds_dbport, rds_engver, rds_licmodel, rds_kname, rds_kval, rds_storetype):

        RDS = self.rds_con
        response = RDS.create_db_instance(
            DBName=rds_db,
            DBInstanceIdentifier=rds_dbinstance,
            AllocatedStorage=rds_dbstore,
            DBInstanceClass=rds_dbinst,
            Engine=rds_dbengine,
            MasterUsername=rds_dbuser,
            MasterUserPassword=rds_dbpwd,
            DBSecurityGroups=[
                rds_sg ,
            ],
            # VpcSecurityGroupIds=[
            #     'string',
            # ],
            AvailabilityZone='string',
            # DBSubnetGroupName='string',
            # PreferredMaintenanceWindow='string',
            # DBParameterGroupName='string',
            # BackupRetentionPeriod=123,
            # PreferredBackupWindow='string',
            Port=rds_dbport,
            MultiAZ=True,
            EngineVersion=rds_engver,
            AutoMinorVersionUpgrade=False,
            LicenseModel=rds_licmodel,
            # Iops=123,
            # OptionGroupName='string',
            # CharacterSetName='string',
            PubliclyAccessible=False,
            Tags=[
                {
                    'Key': rds_kname,
                    'Value': rds_kval
                },
            ],
            # DBClusterIdentifier='string',
            StorageType=rds_storetype,
            # TdeCredentialArn='string',
            # TdeCredentialPassword='string',
            StorageEncrypted=False,
            # KmsKeyId='string',
            # Domain='string',
            CopyTagsToSnapshot=False,
            MonitoringInterval=0,
            # MonitoringRoleArn='string',
            # DomainIAMRoleName='string',
            # PromotionTier=123,
            # Timezone='string'
        )


        return response

    def rds_cluster(self):

        RDS = self.rds_con
        response = RDS.create_db_cluster(
            AvailabilityZones=[
                'string',
            ],
            BackupRetentionPeriod=123,
            CharacterSetName='string',
            DatabaseName='string',
            DBClusterIdentifier='string',
            DBClusterParameterGroupName='string',
            VpcSecurityGroupIds=[
                'string',
            ],
            DBSubnetGroupName='string',
            Engine='string',
            EngineVersion='string',
            Port=123,
            MasterUsername='string',
            MasterUserPassword='string',
            OptionGroupName='string',
            PreferredBackupWindow='string',
            PreferredMaintenanceWindow='string',
            ReplicationSourceIdentifier='string',
            Tags=[
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ],
            StorageEncrypted=True|False,
            KmsKeyId='string'
        )
        return response

        # stackname = raw_input("Enter THE NAME OF THE STACK U REQUIRE : ")vpc-37ee6552
        # stackregion = raw_input("ENTER THE REGOIN OF YOUR DESIRED : ")
        # keyvalue = raw_input("ENTER SSH KEY NAME : ")
        # servicrearn = raw_input("")
        # dfltInstncPrflArn = raw_input("")
        # os = raw_input("ENTER THE OPERATING SYSTEM REQUIRED : ")
        # theme = raw_input("ENTER THE HOST NAME THEME REQUIRED : ")
        # avlbltyzone = raw_input("ENTER AVAILABILITY ZONE : ")
        # v = raw_input("ENTER CHEF VERSION (eg:11,11.4,12(windws:12.5)) : ")
        # brkshf = raw_input("ENTER TRUE OF FALSE OF BERKSHELF : ")
        # if brkshf=='True':
        # bol1= (1==True)
        # elif brkshf=='False':
        # bol1= (0==True)
        # a = len(brkshf)
        # if a < 1:
        # bv = raw_input("ENTER BERKSHELF VERSION : ")
        # cstm = raw_input("ENTER TRUE OR FALSE FOR USE OF CUSTOM COOKBOOKS : ")
        # if cstm=='True':
        # bol2= (1==True)
        # elif cstm=='False':
        # bol2= (0==True)
        # osg = raw_input("ENTER TRUE OR FALSE FOR USE OF OPSSECURITY GROUPS (default)(EXTRA) : ")
        # if osg=='True':
        # bol3= (1==True)
        # elif osg=='False':
        # bol3= (0==True)
        # typ = raw_input("ENTER TYPE OS STORAGE OF YOUR CUSTUMCOOKBOOK :('git'|'svn'|'archive'|'s3') : ")
        # url = raw_input("PASTE THE URL PATH OF YOUR CUSTOM COOKBOOKS : ")
        # usr = raw_input("ENTER USERNAME CUSTOMCOOKBOOKS : ")
        # psw = raw_input("ENTER THE PASSWORD CUSTOMCOOKBOOKS : ")
        # ssh = raw_input("PASTHE THE SSH : ")
        # rvsn = raw_input("REVISION : ")
        # dfltssh = raw_input("IF REQUIRED ENTEER DEFAULT SSH KEY PAIR NAME : ")
        # dfltrootdev = raw_input("ENTER DEFAULT ROOT DEVICE TYPE ('ebs'|'instance-store') : ")
        # ajv = raw_input("ENTER AGENT VERSION : OPS VERSION :: :")

    def create_stack(self, stack_name, stack_region, keyvalue, default_os, hostname_theme, 
        default_availability_zone, chef_version, servicerolearn, default_instance_profile_arn ):
        ''' Ops Works Connection '''
        con = self.opsworks_con
        response = con.create_stack(
            Name = stack_name,
            Region = stack_region,
            # VpcId = vpc_id,
            Attributes = {
                'KeyName': keyvalue
            },
            ServiceRoleArn = servicerolearn,
            DefaultInstanceProfileArn = default_instance_profile_arn,
            DefaultOs = default_os,
            HostnameTheme = hostname_theme,     # by default "Layer_Dependent"
            DefaultAvailabilityZone = default_availability_zone,
            # DefaultSubnetId = 'string',                             #ENTER SUBNET
            # CustomJson = 'string',                                                  #ENTER CUSTOM JSON
            ConfigurationManager = {
                'Name': 'chef',
                'Version': chef_version
            },
            # ChefConfiguration = {
            #     'ManageBerkshelf': bol1,
            #     'BerkshelfVersion': bv
            # },
            UseCustomCookbooks = False
            # UseOpsworksSecurityGroups = bol3,
            # CustomCookbooksSource = {
            #     'Type': usr,
            #     'Url': url,
            #     'Username': usr,
            #     'Password': psw,
            #     'SshKey': ssh,
            #     'Revision': rvsn
            # },
            # DefaultSshKeyName = default_ssh_keyname
            # DefaultRootDeviceType = default_root_devicetype
            # AgentVersion = agent_version
            )
        return response


    def create_layer(self):
        con = self.opsworks_con
        response = con.create_layer(
            StackId='string',
            Type='aws-flow-ruby'|'ecs-cluster'|'java-app'|'lb'|'web'|'php-app'|'rails-app'|'nodejs-app'|'memcached'|'db-master'|'monitoring-master'|'custom',
            Name='string',
            Shortname='string',
            Attributes={
                'string': 'string'
            },
            CustomInstanceProfileArn='string',
            CustomJson='string',
            CustomSecurityGroupIds=[
                'string',
            ],
            Packages=[
                'string',
            ],
            VolumeConfigurations=[
                {
                    'MountPoint': 'string',
                    'RaidLevel': 123,
                    'NumberOfDisks': 123,
                    'Size': 123,
                    'VolumeType': 'string',
                    'Iops': 123
                },
            ],
            EnableAutoHealing=True|False,
            AutoAssignElasticIps=True|False,
            AutoAssignPublicIps=True|False,
            CustomRecipes={
                'Setup': [
                    'string',
                ],
                'Configure': [
                    'string',
                ],
                'Deploy': [
                    'string',
                ],
                'Undeploy': [
                    'string',
                ],
                'Shutdown': [
                    'string',
                ]
            },
            InstallUpdatesOnBoot=True|False,
            UseEbsOptimizedInstances=True|False,
            LifecycleEventConfiguration={
                'Shutdown': {
                    'ExecutionTimeout': 123,
                    'DelayUntilElbConnectionsDrained': True|False
                }
            }
        )

        return response