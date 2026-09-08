# =============================================================================
# COSC2980/2638 Cloud Computing - Assessment 3
# Lambda function: handles a check-in request.
#
# Triggered by: API Gateway POST /checkin
# Writes to: DynamoDB "checkins" table
# Also sends the event to Kinesis, for real-time processing / history.
#
# Expected request body (JSON):
#   { "space_id": "1-2-006", "user_email": "s39260050@student.rmit.edu.au" }
# =============================================================================

import json
import os
from datetime import datetime, timezone

import boto3

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
CHECKINS_TABLE = os.environ.get("CHECKINS_TABLE", "spotcheck_checkins")
KINESIS_STREAM = os.environ.get("KINESIS_STREAM", "spotcheck-events")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
checkins_table = dynamodb.Table(CHECKINS_TABLE)
kinesis = boto3.client("kinesis", region_name=AWS_REGION)


def lambda_handler(event, context):
    body = json.loads(event.get("body") or "{}")
    space_id = body.get("space_id")
    user_email = body.get("user_email")

    if not space_id or not user_email:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "space_id and user_email are required"}),
        }

    timestamp = datetime.now(timezone.utc).isoformat()

    # 1. Record the event in DynamoDB (this becomes the live + historical record)
    checkins_table.put_item(
        Item={
            "space_id": space_id,
            "timestamp": timestamp,
            "status": "checked_in",
            "user_email": user_email,
        }
    )

    # 2. Also push the event to Kinesis, for any real-time consumers
    kinesis.put_record(
        StreamName=KINESIS_STREAM,
        Data=json.dumps({
            "space_id": space_id,
            "user_email": user_email,
            "status": "checked_in",
            "timestamp": timestamp,
        }),
        PartitionKey=space_id,
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"Checked in to {space_id}", "timestamp": timestamp}),
    }