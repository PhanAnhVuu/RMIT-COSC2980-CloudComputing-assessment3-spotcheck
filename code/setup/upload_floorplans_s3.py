# =============================================================================
# COSC2980/2638 Cloud Computing - Assessment 3
# Uploads the RMIT Hanoi Campus floor plan images to S3.
#
# The bucket is created if it does not exist and is left PRIVATE - the app
# will stream images back through an authenticated route, the same pattern
# used for artist images in Assessment 2.
# =============================================================================

import os

import boto3
from botocore.exceptions import ClientError

from config import AWS_REGION, S3_BUCKET

_HERE = os.path.dirname(os.path.abspath(__file__))
FLOORPLANS_DIR = os.path.join(_HERE, os.pardir, os.pardir, "data", "floorplans")

FLOORPLAN_FILES = {
    "floorplans/level-1.jpg": "level-1.jpg",
    "floorplans/level-2.jpg": "level-2.jpg",
    "floorplans/level-3.jpg": "level-3.jpg",
}


def ensure_bucket(s3):
    try:
        s3.head_bucket(Bucket=S3_BUCKET)
        print(f"Bucket '{S3_BUCKET}' already exists.")
        return
    except ClientError as err:
        if err.response["Error"]["Code"] not in ("404", "NoSuchBucket", "403"):
            raise

    kwargs = {"Bucket": S3_BUCKET}
    if AWS_REGION != "us-east-1":
        kwargs["CreateBucketConfiguration"] = {"LocationConstraint": AWS_REGION}
    s3.create_bucket(**kwargs)
    s3.get_waiter("bucket_exists").wait(Bucket=S3_BUCKET)
    print(f"Created bucket '{S3_BUCKET}' in {AWS_REGION}.")


def main():
    s3 = boto3.client("s3", region_name=AWS_REGION)
    ensure_bucket(s3)

    for key, filename in FLOORPLAN_FILES.items():
        path = os.path.join(FLOORPLANS_DIR, filename)
        if not os.path.exists(path):
            print(f"!! Missing file: {path} (skipping {key})")
            continue
        with open(path, "rb") as f:
            s3.put_object(Bucket=S3_BUCKET, Key=key, Body=f.read(), ContentType="image/jpeg")
        print(f"Uploaded {filename} -> s3://{S3_BUCKET}/{key}")


if __name__ == "__main__":
    main()