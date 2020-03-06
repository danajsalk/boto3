# Python boto3
<br>

## Summary: 
<br>
These jupyter scripts show some simple examples for beginner practice interacting with AWS. More automated complex examples should potentially use another service like CloudFormation.

## Before you begin:
<br>

Follow these directions from the boto3 configuration site to set up link between python boto3 and your aws account: 
    * https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration

1. `pip install boto3`
2. configure boto3 to aws
    * If you have the AWS CLI installed, then you can use it to configure your credentials file:
    * `aws configure `
    
    
## Important Notes:
<br>

#### S3 Buckets
* **S3 bucket names are universal and MUST BE UNIQUE**
* **BEST PRACTICE: MAKE S3 BUCKETS PRIVATE**
```
response = client.put_public_access_block(
		    Bucket=my_bucket,
		    PublicAccessBlockConfiguration={
		        'BlockPublicAcls': True,
		        'IgnorePublicAcls': True,
		        'BlockPublicPolicy': True,
		        'RestrictPublicBuckets': True
		    }
		)
 ```
* When uploading files to S3, you have a 5 GB limit. Consider uploading using multi-part transfers
* Use Stubber for Testing

### Response Syntax
* https://docs.aws.amazon.com/AmazonS3/latest/API/API_DeleteObject.html

Response Elements
* If the action is successful, the service sends back an HTTP 204 response.Only returns header

## Useful Links
* Boto3 Selecting Services: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/index.html
* Boto3 Documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/migrations3.html
* Boto3 Testing Stubber: https://botocore.amazonaws.com/v1/documentation/api/latest/reference/stubber.html
