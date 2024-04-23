def versioning(aws_s3_client, bucket_name, status: bool):
    versioning_status = "Enabled" if status else "Suspended"
    aws_s3_client.put_bucket_versioning(
        Bucket=bucket_name, VersioningConfiguration={"Status": versioning_status}
    )
