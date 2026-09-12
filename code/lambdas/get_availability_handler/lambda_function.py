# =============================================================================
# COSC2980/2638 Cloud Computing - Assessment 3
# Lambda function: returns the current availability of every study space.
#
# Triggered by: API Gateway GET /availability
#
# For each space, finds the MOST RECENT check-in/check-out event, and uses
# its status to determine if the space is currently occupied or free.
# =============================================================================

import json
import os

import boto3
from boto3.dynamodb.conditions import Key

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
SPACES_TABLE = os.environ.get("SPACES_TABLE", "spotcheck_spaces")
CHECKINS_TABLE = os.environ.get("CHECKINS_TABLE", "spotcheck_checkins")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
spaces_table = dynamodb.Table(SPACES_TABLE)
checkins_table = dynamodb.Table(CHECKINS_TABLE)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json",
}


def latest_event(space_id):
    result = checkins_table.query(
        KeyConditionExpression=Key("space_id").eq(space_id),
        ScanIndexForward=False,
        Limit=1,
    )
    items = result.get("Items", [])
    return items[0] if items else None


def lambda_handler(event, context):
    spaces = spaces_table.scan().get("Items", [])

    results = []
    for space in spaces:
        latest = latest_event(space["space_id"])
        if latest and latest.get("status") == "checked_in":
            status = "occupied"
            checked_in_by = latest.get("user_email")
        else:
            status = "available"
            checked_in_by = None

        results.append({
            "space_id": space["space_id"],
            "name": space["name"],
            "floor": space["floor"],
            "building": space["building"],
            "status": status,
            "checked_in_by": checked_in_by,
        })

    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": json.dumps({"spaces": results}),
    }