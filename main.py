import argparse
import boto3
from botocore.exceptions import ClientError

# Create the parser
parser = argparse.ArgumentParser(description="Argument parser")

# Add arguments
parser.add_argument("--bucket", type=str, help="Bucket name")
parser.add_argument(
    "-be", "--bucket_exists", action="store_true", help="Check if bucket exists"
)
parser.add_argument("-lb", "--list_buckets", action="store_true", help="List buckets")
parser.add_argument(
    "-db", "--delete_bucket", action="store_true", help="Delete a bucket"
)
parser.add_argument(
    "-cb", "--create_bucket", action="store_true", help="Create a bucket"
)
parser.add_argument(
    "-lo", "--list_objects", action="store_true", help="List objects in a bucket"
)


def init_client():
    try:
        client = boto3.client(
            "s3",
            aws_access_key_id="",
            aws_secret_access_key="",
            aws_session_token="",
            region_name="us-east-1",
        )
        client.list_buckets()
        return client
    except ClientError as e:
        print(e)


def bucket_exists(aws_s3_client, bucket_name) -> bool:
    try:
        response = aws_s3_client.head_bucket(Bucket=bucket_name)
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code == 200:
            return True
    except ClientError as e:
        print(e)
        return False


def list_buckets(aws_s3_client):
    response = aws_s3_client.list_buckets()
    for bucket in response["Buckets"]:
        print(bucket["Name"])


def delete_bucket(aws_s3_client, bucket_name):
    try:
        aws_s3_client.delete_bucket(Bucket=bucket_name)
    except ClientError as e:
        print(e)
        return False
    return True


def create_bucket(aws_s3_client, bucket_name, region="us-east-2") -> bool:
    location = {"LocationConstraint": region}
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/create_bucket.html
    response = aws_s3_client.create_bucket(
        Bucket=bucket_name, CreateBucketConfiguration=location
    )
    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    if status_code == 200:
        return True
    return False


def get_objects(aws_s3_client, bucket_name) -> str:
    for key in aws_s3_client.list_objects(Bucket=bucket_name)["Contents"]:
        print(f" {key['Key']}, size: {key['Size']}")


if __name__ == "__main__":
    # Parse the arguments
    args = parser.parse_args()

    s3_client = init_client()

    # List buckets
    if args.list_buckets:
        list_buckets(s3_client)

    # Check bucket existence
    if args.bucket_exists:
        print(f"Bucket exists: {bucket_exists(s3_client, args.bucket)}")

    # Create bucket
    if args.create_bucket:
        print(f"Bucket created: {create_bucket(s3_client, args.bucket)}")

    # Delete bucket
    if args.delete_bucket:
        print(f"Bucket deleted: {delete_bucket(s3_client, args.bucket)}")

    # List objects
    if args.list_objects:
        get_objects(s3_client, args.bucket)
