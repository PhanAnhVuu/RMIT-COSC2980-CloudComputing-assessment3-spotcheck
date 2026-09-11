# =============================================================================
# COSC2980/2638 Cloud Computing - Assessment 3
# Lambda function: handles user login.
#
# Triggered by: API Gateway POST /login
#
# Expected request body (JSON):
#   { "email": "...", "password": "..." }
# =============================================================================

import json
import os

import boto3

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
USERS_TABLE = os.environ.get("USERS_TABLE", "spotcheck_users")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
users_table = dynamodb.Table(USERS_TABLE)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json",
}


def lambda_handler(event, context):
    body = json.loads(event.get("body") or "{}")
    email = body.get("email", "").strip()
    password = body.get("password", "")

    item = users_table.get_item(Key={"email": email}).get("Item")

    if item is None or item.get("password") != password:
        return {
            "statusCode": 401,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "email or password is invalid"}),
        }

    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": json.dumps({
            "message": "Login successful",
            "email": item["email"],
            "user_name": item.get("user_name", item["email"]),
        }),
    }