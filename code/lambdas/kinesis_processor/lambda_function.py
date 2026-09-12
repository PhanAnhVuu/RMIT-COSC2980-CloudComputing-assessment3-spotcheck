# =============================================================================
# COSC2980/2638 Cloud Computing - Assessment 3
# Lambda function: Kinesis stream consumer.
#
# Triggered automatically by AWS whenever new records arrive on the
# "spotcheck-events" Kinesis stream (not triggered via API Gateway).
#
# For every check-in event, increments a daily counter per space in the
# "spotcheck_activity_counts" table - this is a live, real-time aggregation
# that is genuinely separate from the raw event log in "checkins".
# =============================================================================

import base64
import json
import os
from datetime import datetime, timezone

import boto3

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
ACTIVITY_TABLE = os.environ.get("ACTIVITY_TABLE", "spotcheck_activity_counts")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
activity_table = dynamodb.Table(ACTIVITY_TABLE)


def lambda_handler(event, context):
    for record in event["Records"]:
        # Kinesis record data arrives base64-encoded.
        payload = base64.b64decode(record["kinesis"]["data"])
        data = json.loads(payload)

        if data.get("status") != "checked_in":
            continue   # only count check-ins, not check-outs

        space_id = data["space_id"]
        date = data["timestamp"][:10]   # "2026-09-11T..." -> "2026-09-11"

        activity_table.update_item(
            Key={"space_id": space_id, "date": date},
            UpdateExpression="ADD checkin_count :one",
            ExpressionAttributeValues={":one": 1},
        )

    return {"statusCode": 200}