import boto3, os

account = os.environ["AWS_ACCOUNT_ID"]
region = os.environ["AWS_DEFAULT_REGION"]

# unique job name
job_name_prefix = 'mlops-scikit-bring-your-own'
build_version = '-v' + os.environ['CODEBUILD_BUILD_NUMBER']
job_name = job_name_prefix + build_version

# train info
container = '{}.dkr.ecr.{}.amazonaws.com/mlops-scikit_bring_your_own:latest'.format(account, region) 
role = 'arn:aws:iam::{}:role/SageMakerExecutionRole'.format(account)

bucket = 's3://' + 'sagemaker-datalake-' + region + account
# input_data = bucket + '/iris/input/iris.csv'
input_data = bucket + '/iris/input/'
output_location = bucket + '/iris/output'

train_instance_type = 'ml.c4.2xlarge'
train_instance_count = 1
use_spot_instances = True

# trigger job training
# tree = sagemaker.estimator.Estimator(image, 
#     role,
#     train_instance_count,
#     train_instance_type,
#     use_spot_instances=use_spot_instances,
#     max_wait=86400,
#     output_path=output_location, 
#     sagemaker_session=sagemaker.Session()) 
# tree.fit(inputs=data_location, job_name=job_name, wait=False)

# print('job created with name: ' + job_name)

sagemaker = boto3.client('sagemaker')

def create_training_job(job_name, input_data, container, output_location):
    try:
        response = sagemaker.create_training_job(
            TrainingJobName=job_name,
            AlgorithmSpecification={
                'TrainingImage': container,
                'TrainingInputMode': 'File',
            },
            RoleArn=role,
            InputDataConfig=[
                {
                    'ChannelName': 'train',
                    'DataSource': {
                        'S3DataSource': {
                            'S3DataType': 'S3Prefix',
                            'S3Uri': input_data,
                            'S3DataDistributionType': 'FullyReplicated'
                        }
                    },
                    'ContentType': 'text/csv',
                    'CompressionType': 'None'
                }
            ],
            OutputDataConfig={
                'S3OutputPath': output_location
            },
            ResourceConfig={
                'InstanceType': train_instance_type,
                'InstanceCount': train_instance_count,
                'VolumeSizeInGB': 20
            },
            StoppingCondition={
                'MaxRuntimeInSeconds': 3600,
                'MaxWaitTimeInSeconds': 3600
            },
            EnableManagedSpotTraining=True
        )
        print(response)

    except Exception as e:
        print(e)
        print('Unable to create training job.')
        raise(e)

def create_model(model_name, container):
    try:
        response = sagemaker.create_model(
            ModelName=model_name,
            ExecutionRoleArn=role,
            PrimaryContainer={
                'Image': container,
                'ModelDataUrl': output_location
            }
        )
        print(response)

    except Exception as e:
        print(e)
        print('Unable to create model.')
        raise(e)


# create model
# model_name = job_name


# create_model_response = sagemaker.create_model(
#     ModelName=model_name,
#     ExecutionRoleArn=role,
#     PrimaryContainer={
#         'Image': container_image,
#         'ModelDataUrl': output_location})

# print(create_model_response['ModelArn'])

create_training_job(job_name, input_data, container, output_location)
create_model(job_name, container)