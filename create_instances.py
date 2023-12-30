import boto3
import config

# This is a code that:
#   - Creates a security group
#   - Launches 5 EC2 instances of type t2.micro
#   - Launches 2 EC2 instances of type t2.large

# AWS credentials
aws_access_key_id = config.aws_access_key_id
aws_secret_access_key = config.aws_secret_access_key
aws_session_token = config.aws_session_token


# Initializes an EC2 client
ec2 = boto3.client('ec2',
                   aws_access_key_id=aws_access_key_id,
                   aws_secret_access_key=aws_secret_access_key,
                   aws_session_token=aws_session_token,
                   region_name=config.region_name)

# Creates a security group
security_group_name = config.security_group_name
security_group = ec2.create_security_group(
    GroupName=security_group_name,
    Description='Security group for Final project'
)
sg_id = security_group['GroupId']

# Associated with creation of security group
ec2.authorize_security_group_ingress(
    GroupId=sg_id,
    IpProtocol='tcp',
    FromPort=22,
    ToPort=22,
    CidrIp='0.0.0.0/0'
)

# Associated with creation of security group
ec2.authorize_security_group_ingress(
    GroupId=sg_id,
    IpProtocol='tcp',
    FromPort=80,
    ToPort=80,
    CidrIp='0.0.0.0/0'
)

# Associated with creation of security group
ec2.authorize_security_group_ingress(
    GroupId=sg_id,
    IpProtocol='tcp',
    FromPort=5000,
    ToPort=5002,
    CidrIp='0.0.0.0/0'
)

# Launching 5 EC2 instances of type t2.micro
no_instances_micro = 5
instances_micro = ec2.run_instances(
    ImageId='ami-053b0d53c279acc90',
    InstanceType='t2.micro',
    MaxCount=no_instances_micro,
    MinCount=no_instances_micro,
    Placement={'AvailabilityZone': 'us-east-1a'},
    KeyName=config.key_name,
    SecurityGroups=[security_group_name],
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/sda1',  # The root volume
            'Ebs': {
                'VolumeSize': 15,  # Specify the size of the root volume in GB
                'VolumeType': 'gp2'  # Specify the volume type (e.g., gp2, io1, standard)
            },
        },
    ]
)

# Launching 2 EC2 instances of type t2.large
no_instances_large = 2
instances_large = ec2.run_instances(
    ImageId='ami-053b0d53c279acc90',
    InstanceType='t2.large',
    MaxCount=no_instances_large,
    MinCount=no_instances_large,
    Placement={'AvailabilityZone': 'us-east-1a'},
    KeyName=config.key_name,
    SecurityGroups=[security_group_name],
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/sda1',  # The root volume
            'Ebs': {
                'VolumeSize': 15,  # Specify the size of the root volume in GB
                'VolumeType': 'gp2'  # Specify the volume type (e.g., gp2, io1, standard)
            },
        },
    ]
)

# Message when the instances are created
ec2_waiter = ec2.get_waiter('instance_running')
for instance in instances_micro['Instances'] + instances_large['Instances']:
    instance_id = instance['InstanceId']
    ec2_waiter.wait(InstanceIds=[instance_id])
print('Instances running')
