#!/usr/bin/python

import boto3
import os

region = "us-east-1"
aws_key_env_var = 'aws_key'
aws_secret_env_var = 'aws_secret'

aws_key = os.environ.get(aws_key_env_var)
aws_secret_key = os.environ.get(aws_secret_env_var)
aws_session = boto3.session.Session(aws_access_key_id=aws_key,aws_secret_access_key=aws_secret_key,region_name=region)

s3 = aws_session.resource('s3')
total_size = 0
bytes_per_gb = 1073741824

for bucket in s3.buckets.all():
    bucket_mpu_gb = 0
    try:
        for mpu in bucket.multipart_uploads.all():
            mpu_size = 0
            try:
                for part in mpu.parts.all():
                    mpu_size += part.size
                    mpu_gb = mpu_size / bytes_per_gb
                    print(bucket.name+","+str(mpu.initiated)+','+mpu.object_key+','+str(mpu_gb))
                bucket_mpu_gb += mpu_gb
            except:
                continue
        print("bucket",bucket.name,bucket_mpu_gb,"GB")
    except:
        continue
    total_size += bucket_mpu_gb

print("Total GB's of space in failed multipart uploads",total_size)

#for readabilty its better to get the list of buckets and try execpt that then iterate over the buckets and try execpt if there is a failue in the phase of the code execution
