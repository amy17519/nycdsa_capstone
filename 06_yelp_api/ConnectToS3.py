# Connecting to S3 bucket

from boto.s3.connection import S3Connection

AWS_KEY = 'AKIAIDZXQYUBMMS6WHRA'
AWS_SECRET = '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'
aws_connection = S3Connection(AWS_KEY, AWS_SECRET)
bucket = aws_connection.get_bucket('yelpcapstone')
for file_key in bucket.list():
   print file_key.name

key = list(bucket.list())[-1]
type(key)
