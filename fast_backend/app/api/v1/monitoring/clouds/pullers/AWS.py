#import boto3
import os
import sys
from app.utils.db_utils import *
import traceback
import boto3
# from app.mail import GenerateMailForCloudAlert


def ResolveARN(lb_arn):
    try:
        lbarray = lb_arn.split(':')
        lbstring = lbarray[-1]
        lbarray2 = lbstring.split('/')
        lbstring2 = lbarray2[1] + '/' + lbarray2[2] + '/' + lbarray2[3]

        return lbstring2
    except Exception:
        return ""


class AWS:
    def __init__(self, access_key, secret_key, account_label):
        self.access_key = access_key
        self.secret_key = secret_key
        self.account_label = account_label
        self.access_type = self.GetAccessType()
        self.session = self.GetConnection()

    def GetAccessType(self):
        session = boto3.Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key)
        iam = session.client('iam')
        try:
            user = iam.get_user()
            username = user['User']['UserName']
            response = iam.list_attached_user_policies(UserName=username)
            for policy in response['AttachedPolicies']:
                if policy['PolicyArn'] == 'arn:aws:iam::aws:policy/AdministratorAccess':
                    print(f'{username} : User has the AdministratorAccess permission policy', file=sys.stderr)
                    return "Admin"
            else:
                print(f'{username} : User does not have the AdministratorAccess permission policy', file=sys.stderr)
                return "Non-Admin"
        except Exception as e:
            print(e, file=sys.stderr)
            print(f'Error : User does not have the AdministratorAccess permission policy', file=sys.stderr)
            return "Non-Admin"

    def TestConnection(self):
        try:
            session = boto3.Session(
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key)
            client = session.client('sts')
            client.get_caller_identity()
            return True
        except Exception as e:
            return False

    def GetConnection(self):
        session = boto3.Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key)
        try:
            client = session.client('sts')
            client.get_caller_identity()
            return session
        except Exception:
            return None

    def GetAllEC2(self):
        instances = []
        for region in self.session.get_available_regions('ec2'):
            try:
                ec2 = self.session.client('ec2', region_name=region)
                response = ec2.describe_instances()

                for reservation in response["Reservations"]:
                    for instance in reservation["Instances"]:
                        name = ''
                        for tag in instance['Tags']:
                            if tag['Key'] == 'Name':
                                name = tag['Value']
                                break
                        instances.append(
                            {
                                "instance_name": name,
                                "instance_id": instance['InstanceId'],
                                "state": instance['State']['Name'],
                                "region_id": region
                            }
                        )
            except Exception as e:
                print("Error in " + region, file=sys.stderr)

        return instances

    def GetAllS3(self):
        buckets = []
        try:
            s3_client = self.session.client('s3')
            response = s3_client.list_buckets()
            for bucket in response['Buckets']:
                bucket_name = bucket['Name']
                location = s3_client.get_bucket_location(Bucket=bucket_name)[
                    'LocationConstraint']

                print(f"{bucket_name}: {location}", file=sys.stderr)

                buckets.append(
                    {'bucket_name': bucket_name, 'region_id': location})

        except Exception as e:
            print(e, file=sys.stderr)

        return buckets

    def GetAllELB(sefl):

        instances = []
        for region in sefl.session.get_available_regions('elbv2'):
            try:
                ec2 = sefl.session.client('elbv2', region_name=region)
                response = ec2.describe_load_balancers()

                for lb in response['LoadBalancers']:

                    lb_arn = ResolveARN(lb['LoadBalancerArn'])
                    if lb_arn == "":
                        pass
                    else:
                        instances.append(
                            {
                                'lb_arn': lb_arn,
                                'lb_name': lb['LoadBalancerName'],
                                'lb_type': lb['Type'],
                                'lb_scheme': lb['Scheme'],
                                'lb_dns': lb['DNSName'],
                                "region_id": region
                            }
                        )
            except Exception as e:
                print("Error in " + region, file=sys.stderr)

        return instances

    def GetAllRDS(self):
        rdsList = []
        for region in self.session.get_available_regions('rds'):
            try:
                # Retrieve all RDS instances
                rds = self.session.client('rds', region_name=region)
                response = rds.describe_db_instances()

                for db in response['DBInstances']:
                    print(db)
                    rdsObj = {
                        'rds_name': db['DBInstanceIdentifier'],
                        'rds_class': db['DBInstanceClass'],
                        'rds_engine': db['Engine'],
                        'rds_status': db['DBInstanceStatus'],
                        'region_id': region,
                    }

                    rdsList.append(rdsObj)

                    print(rdsObj, file=sys.stderr)

            except Exception as e:
                print("Error in " + region, file=sys.stderr)
        return rdsList

    def GetAllEKS(self):
        clusters = []
        for region in self.session.get_available_regions('eks'):
            try:
                eks = self.session.client('eks', region_name=region)
                response = eks.list_clusters()

                for cluster in response['clusters']:
                    clusters.append({'cluster': cluster,
                                     'region_id': region})

            except Exception as e:
                print(e, file=sys.stderr)
                print("Error in " + region, file=sys.stderr)

        return clusters

    # def GetAllVPC(self):
    #     vpc_list = []
    #     for region in self.session.get_available_regions('ec2'):
    #         try:
    #             ec2_client = self.session.client('ec2', region_name=region)

    #             # Use the client to get a list of all VPCs in the account
    #             response = ec2_client.describe_vpcs()

    #             # Extract the VPC IDs from the response
    #             for vpc in response['Vpcs']:
    #                 vpc_list.append({
    #                     'vpc_id': vpc['VpcId'],
    #                     'state': vpc['State'],
    #                     'region_id': region
    #                 })
    #         except Exception as e:
    #             print("Error in "+region)

    #     return vpc_list

    def WriteAlert(self, alertObj):
        try:
            query = f"select * from aws_alerts_table where SERVICE_NAME = '{alertObj['service_name']}' and SERVICE_KEY='{alertObj['service_key']}' and `TYPE` = '{alertObj['type']}' and `STATUS` ='Open';"
            ec2Alert = db.session.execute(query).fetchone()

            if ec2Alert is not None:

                # Clearing the alert
                if (ec2Alert[4] == "Critical" or ec2Alert[4] == "High") and alertObj['level'] == 'Normal':
                    query = f"update aws_alerts_table set `STATUS` = 'Clear' , MODIFICATION_DATE = '{alertObj['time']}' where SERVICE_NAME = '{alertObj['service_name']}' and SERVICE_KEY='{alertObj['service_key']}' and `TYPE` = '{alertObj['type']}' and `STATUS` ='Open';"
                    configs.db.execute(query)
                    configs.db.commit()

                    alertObj['status'] = "Clear"
                    alertObj['account_label'] = self.account_label
                    GenerateMailForCloudAlert(alertObj)
                else:
                    query = f"update aws_alerts_table set `LEVEL` = '{alertObj['level']}', DESCRIPTION = '{alertObj['description']}',STATUS='Open', MODIFICATION_DATE='{alertObj['time']}' where SERVICE_NAME = '{alertObj['service_name']}' and SERVICE_KEY='{alertObj['service_key']}' and `TYPE` = '{alertObj['type']}' and `STATUS` ='Open';"
                    configs.db.execute(query)
                    configs.db.commit()

            elif alertObj['level'] == 'Critical' or alertObj['level'] == 'High':
                query = f"INSERT INTO aws_alerts_table (`SERVICE_NAME`, `SERVICE_KEY`, `ACCOUNT_LABEL`, `LEVEL`, `TYPE`, `DESCRIPTION`, `CREATETION_DATE`, `MODIFICATION_DATE`) VALUES ('{alertObj['service_name']}', '{alertObj['service_key']}', '{self.account_label}', '{alertObj['level']}', '{alertObj['type']}', '{alertObj['description']}', '{alertObj['status']}', '{alertObj['time']}', '{alertObj['time']}');"
                configs.db.execute(query)
                configs.db.commit()

                alertObj['status'] = "Open"
                alertObj['account_label'] = self.account_label
                GenerateMailForCloudAlert(alertObj)

        except Exception as e:
            print("Error In AWS Alert", file=sys.stderr)
            traceback.print_exc()
            print(e, file=sys.stderr)
