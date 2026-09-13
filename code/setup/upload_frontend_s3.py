# =============================================================================
# COSC2980/2638 Cloud Computing - Assessment 3
# Uploads the frontend files (HTML/CSS/JS) to S3, so CloudFront can serve
# them to the public internet.
# =============================================================================

import os

import boto3

from config import AWS_REGION, S3_BUCKET

_HERE = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(_HERE, os.pardir, "frontend")

FILES = {
    "frontend/index.html": ("index.html", "text/html"),
    "frontend/style.css": ("style.css", "text/css"),
    "frontend/app.js": ("app.js", "application/javascript"),
}


def main():
    s3 = boto3.client("s3", region_name=AWS_REGION)

    for key, (filename, content_type) in FILES.items():
        path = os.path.join(FRONTEND_DIR, filename)
        with open(path, "rb") as f:
            s3.put_object(Bucket=S3_BUCKET, Key=key, Body=f.read(), ContentType=content_type)
        print(f"Uploaded {filename} -> s3://{S3_BUCKET}/{key}")


if __name__ == "__main__":
    main()