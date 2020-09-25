import boto3, sys
from urllib.parse import urlparse

model_name = sys.argv[1]
md_bucket = sys.argv[2]
job_name = sys.argv[3]

sagemaker = boto3.client('sagemaker')
s3 = boto3.client('s3')
account_id = boto3.client('sts').get_caller_identity()['Account']

# Config model parameters
resp = sagemaker.describe_training_job(TrainingJobName=job_name)

md_data_url = resp['ModelArtifacts']['S3ModelArtifacts']
container_image = resp['AlgorithmSpecification']['TrainingImage']
role = 'arn:aws:iam::{}:role/SageMakerExecutionRole'.format(account_id)

# Create model
create_model_response = sagemaker.create_model(
    ModelName=model_name,
    ExecutionRoleArn=role,
    PrimaryContainer={
        'Image': container_image,
        'ModelDataUrl': md_data_url})

print(create_model_response['ModelArn'])


