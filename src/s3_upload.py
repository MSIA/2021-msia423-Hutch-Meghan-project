import boto3
import logging.config

# configure logging
logger = logging.getLogger(__name__)
logger.setLevel("INFO")

# use boto3 to upload annotated tweets to S3 bucket
boto3.set_stream_logger('botocore', level='DEBUG')
s3 = boto3.resource("s3")
bucket = s3.Bucket("2021-msia423-hutch-meghan")
bucket.upload_file("data/sample/tweets.csv", "data/sample_tweets.csv")

