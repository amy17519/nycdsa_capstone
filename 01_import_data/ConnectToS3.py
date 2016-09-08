# Connecting to S3 bucket

import io
import json
from boto.s3.connection import S3Connection

credentials_file = 's3_credentials.json'
# AWS IAM credentials
with io.open(credentials_file) as cred:
    creds = json.load(cred)
AWS_KEY = creds['AWS_KEY']
AWS_SECRET = creds['AWS_SECRET']

# Establish connection
aws_connection = S3Connection(AWS_KEY, AWS_SECRET)
bucket = aws_connection.get_bucket('yelpcapstone')
for file_key in bucket.list():
    print file_key.name

key = list(bucket.list())[-1]
type(key)

# Push files to yelpcapstone bucket on AWS

