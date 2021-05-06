import boto3

# use boto3 to upload annotated tweets to S3 bucket
s3 = boto3.resource("s3")
bucket = s3.Bucket("2021-msia423-hutch-meghan")
bucket.upload_file("../data/external/constructs.csv", "data/tweets.csv")

