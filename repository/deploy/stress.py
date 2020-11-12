
from sagemaker.serializers import CSVSerializer
import pandas as pd 
import time 
import boto3

sm = boto3.client("sagemaker-runtime")
endpoint_name = 'scikit-bring-your-own'

def predict(payload):
    csv_serializer = CSVSerializer()
    payload = payload
    X = payload[:,1:]
    y = payload[:,0]
    elapsed_time = time.time()
    resp = sm.invoke_endpoint(
                             EndpointName= endpoint_name,
                             ContentType='text/csv',
                             Accept='text/csv',
                             Body=csv_serializer.serialize(X)
                             )
    elapsed_time = time.time() - elapsed_time
    resp = resp['Body'].read().decode('utf-8').strip()
    return elapsed_time

df = pd.read_csv('iris.csv')
et = predict(df.to_numpy())
print(et)
