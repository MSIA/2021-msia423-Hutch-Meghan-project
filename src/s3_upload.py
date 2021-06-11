import argparse

import boto3
import botocore
import re
import logging.config

# configure logging
logger = logging.getLogger(__name__)
logger.setLevel("INFO")

# use boto3 to upload annotated tweets to S3 bucket
boto3.set_stream_logger('botocore', level='DEBUG')

# parse_s3 function written in the MSIA-423/aws-s3 tutorial
def parse_s3(s3path_str):
    """Parse the S3 path and derive S3 bucket and S3 path.
    
    Args:
        s3path_str: str - name and path of the S3 bucket.
    
    Returns: 
        s3bucket: str - parsed name of the S3 bucket.
        s3path: str - parsed path where the data in S3 is stored.
    
    """
    
    regex = r"s3://([\w._-]+)/([\w./_-]+)"

    m = re.match(regex, s3path)
    s3bucket = m.group(1)
    s3_local_path = m.group(2)

    return s3bucket, s3_local_path

def connect_s3(connect_type, s3path, local_path):
    """Connect to S3 bucket to upload or download data.
    
    Args:
        connect_type: str - parameter takes in "upload" or "download" to perform desired action.
        s3path: str - indicate the name of the S3 bucket.
        local_path: str - indicate the local path to download data to.

    Returns: None.

    """
    
    if connect_type == 'upload':
        
        s3bucket, s3_local_path = parse_s3(s3path)
        s3 = boto3.resource("s3")
        logger.debug('Connect to S3 Bucket')
        bucket = s3.Bucket(s3bucket)
        bucket.upload_file("data/external/constructs.csv", s3_local_path)
        logger.info('Data uploaded to S3 bucket.')
    
    elif connect_type == 'download':
        
        s3bucket, s3_local_path = parse_s3(s3path)
        s3 = boto3.resource("s3")
        logger.debug('Connect to S3 Bucket')
        bucket = s3.Bucket(s3bucket)
        logger.info('Data downloaded from S3 bucket.')
        
        # use the parsed S3 path to identify path to download file from
        try:
            bucket.download_file(s3_local_path, local_path)
        except botocore.exceptions.NoCredentialsError:
            logger.error('Please provide AWS credentials via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables.')
        else:
            logger.info('Data downloaded from %s to %s', s3path, local_path)
