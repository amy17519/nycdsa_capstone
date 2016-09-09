# Connecting to S3 bucket
def s3_connect(credentials_file, bucket_name):
    import io
    import json
    from boto.s3.connection import S3Connection

    # AWS IAM credentials
    with io.open(credentials_file) as cred:
        creds = json.load(cred)
    aws_key = creds['AWS_KEY']
    aws_secret = creds['AWS_SECRET']

    # Establish connection
    aws_connection = S3Connection(aws_key, aws_secret)
    aws_bucket = aws_connection.get_bucket(bucket_name)
    for file_key in bucket.list():
        print file_key.name
    return aws_bucket


# Push files to yelpcapstone bucket on AWS
def s3_upload(filename, s3_bucket):
    import sys
    from boto.s3.key import Key

    def percent_cb(complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()

    print 'Uploading %s to Amazon S3 bucket %s' % (filename, s3_bucket.name)
    bk = Key(s3_bucket)
    bk.key = filename
    bk.set_contents_from_filename(filename, cb=percent_cb, num_cb=10)
    print 'Done'


# Delete files in AWS bucket
def s3_delete(filename, s3_bucket):
    from boto.s3.key import Key
    bk = Key(s3_bucket)
    bk.key = filename
    s3_bucket.delete_key(bk)


# Example use
capstone_creds = 's3_credentials.json'
capstone_bucket = 'yelpcapstone'

bucket = s3_connect(capstone_creds, capstone_bucket)
s3_upload('ImportData.py', bucket)
s3_delete('ImportData.py', bucket)

# Example of s3_credentials.json
# {
#   "AWS_KEY": "DAVIDBBV6J626S6NUUVQ",
#   "AWS_SECRET": "1mJzDFjkors3tgHqlAev5XJbkWkVe+VZobQjRcBH"
# }
