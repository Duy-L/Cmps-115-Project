from storages.backends.s3boto3 import S3Boto3Storage

#this takes care of our static pictures and media pictures and upload to the AWS S3 cloud
StaticRootS3BotoStorage = lambda: S3Boto3Storage(location='static')
MediaRootS3BotoStorage  = lambda: S3Boto3Storage(location='media')
