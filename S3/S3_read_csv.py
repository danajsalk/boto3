import boto3
import codecs
import csv
import pandas as pd

#boto3.setup_default_session(profile_name='PERMISSIONS-PROFILE')

bucket                 = 'BUCKET-NAME-HERE'
prefix                 = 'PREFIX/GOES/HERE'

s3c = boto3.client("s3")


my_bucket = s3_resource.Bucket(bucket)

all_dat = []
objs = [obj.key for obj in my_bucket.objects.filter(Prefix=prefix)]

ct = 0
for obj in my_bucket.objects.filter(Prefix=prefix):
    if (obj.key).endswith('.csv'):
        ct += 1
        print(ct,'/', len(objs), ':', obj.key)
        data = s3c.get_object(Bucket=bucket, Key=obj.key)

        for row in csv.DictReader(codecs.getreader("utf-8")(data["Body"])):
            all_dat.append(row)
        
df = pd.DataFrame(all_dat)
