# =============================================================================
# COSC2980/2638 Cloud Computing - Assessment 3
# Exports all DynamoDB "checkins" records to a CSV file in S3, so Athena can
# query them for historical trend analysis.
#
# In a production system this would run on a schedule (e.g. via EventBridge);
# for this project it's run manually whenever fresh data should be analysed.
# =============================================================================

import csv
import io

import boto3

from config import AWS_REGION, CHECKINS_TABLE, S3_BUCKET

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
s3 = boto3.client("s3", region_name=AWS_REGION)


def scan_all(table):
    result = table.scan()
    items = result.get("Items", [])
    while "LastEvaluatedKey" in result:
        result = table.scan(ExclusiveStartKey=result["LastEvaluatedKey"])
        items.extend(result.get("Items", []))
    return items


def main():
    table = dynamodb.Table(CHECKINS_TABLE)
    items = scan_all(table)
    print(f"Read {len(items)} records from '{CHECKINS_TABLE}'.")

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["space_id", "timestamp", "status", "user_email"])
    for item in items:
        writer.writerow([
            item.get("space_id", ""),
            item.get("timestamp", ""),
            item.get("status", ""),
            item.get("user_email", ""),
        ])

    key = "athena-data/checkins/checkins.csv"
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=buffer.getvalue().encode("utf-8"))
    print(f"Uploaded to s3://{S3_BUCKET}/{key}")


if __name__ == "__main__":
    main()