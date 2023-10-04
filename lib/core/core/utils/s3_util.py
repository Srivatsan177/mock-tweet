import boto3
import os

S3_BUCKET = os.environ["S3_BUCKET"]
URL_EXPIRE_SECONDS = 60 * 5  # 5 minutes
s3_client = boto3.client("s3")


def get_s3_presigned_url(path, method):
    s3_url = s3_client.generate_presigned_url(
        method,
        Params={
            'Bucket': S3_BUCKET,
            'Key': path
        },
        ExpiresIn=URL_EXPIRE_SECONDS
    )
    return s3_url
