def create_model(model_name, model_data_url, model_image, source_directory, region_name, role):
    sagemaker_client = boto3.client('sagemaker', region_name=region_name)
    try:
        container = { 
                        'Image': model_image, 
                        'ModelDataUrl': model_data_url,
                        'Mode': 'MultiModel' ,
                        'MultiModelConfig': {
                                'ModelCacheSetting': 'Disabled' #default enabled
                        }
                   }

        response = sagemaker_client.create_model(
                      ModelName        = model_name,
                      ExecutionRoleArn = role,
                      Containers       = [container]
                    )
        print("CREATED MODEL: ", model_name)
    except:
        print("MODEL ALREADY CREATED: ", model_name)
    
def create_endpoint_config(config_name, model_name, region_name):
    sagemaker_client = boto3.client('sagemaker', region_name=region_name)
    
    try:
        response = sagemaker_client.create_endpoint_config(
                    EndpointConfigName = config_name,
                    ProductionVariants=[
                         {
                            'InstanceType':        'ml.c5.xlarge',
                            'InitialInstanceCount': 2,
                            'InitialVariantWeight': 1,
                            'ModelName':            model_name,
                            'VariantName':          'AllTraffic'
                          }
                    ]
               )
        print("CREATED ENDPOINT CONFIG: ", config_name)
    except:
        print("ENDPOINT CONFIG ALREADY CREATED: ", config_name)

def create_endpoint(endpoint_name, config_name, region_name):
    sagemaker_client = boto3.client('sagemaker', region_name=region_name)
    
    try:
        response = sagemaker_client.create_endpoint(
                      EndpointName       = endpoint_name,
                      EndpointConfigName = config_name)
        print("CREATED ENDPOINT: ", endpoint_name)
    except:
        print("ENDPOINT ALREADY CREATED: ", endpoint_name)
        
bucket = 'BUCKET_NAME'
model_prefix = 'prefix/models/'
direct_prefix = 'prefix/source/sourcedir.tar.gz'

model_data_url = "s3://{}/{}".format(bucket, model_prefix)
source_directory = "s3://{}/{}".format(bucket, direct_prefix)

role = 'arn:aws:iam::{ACCOUNT_ID}:role/service-role/role'

model_name = 'b3-mme-model-TEST'
model_image = "246618743249.dkr.ecr.us-west-2.amazonaws.com/sagemaker-scikit-learn:1.0-1-cpu-py3"
create_model(model_name, model_data_url, model_image, source_directory, region_name, role)

config_name = 'b3-mme-config-TEST'
create_endpoint_config(config_name, model_name, region_name)

endpoint_name = 'b3-mme-TEST'
create_endpoint(endpoint_name, config_name, region_name)

#waiter = sagemaker_client.get_waiter('endpoint_in_service')
#waiter.wait(EndpointName=endpoint_name)

#delete_infra(model_name, config_name, endpoint_name)