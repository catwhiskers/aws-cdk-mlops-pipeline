npm install 

account=$(aws sts get-caller-identity --query Account --output text)
region=$(aws configure get region)
echo $account $region
cdk bootstrap aws://${account}/${region}


echo "upload data to s3"
aws s3 cp data/iris.csv s3://sagemaker-datalake-${region}-${account}/iris/input/iris.csv

