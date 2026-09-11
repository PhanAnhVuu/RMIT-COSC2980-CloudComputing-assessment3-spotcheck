# =============================================================================
# COSC2980/2638 Cloud Computing - Assessment 3
# Lambda function: handles user registration.
#
# Triggered by: API Gateway POST /register
#
# Expected request body (JSON):
#   { "email": "...", "user_name": "...", "password": "..." }
# =============================================================================

import json
import os

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

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
    user_name = body.get("user_name", "").strip()
    password = body.get("password", "")

    if not email or not user_name or not password:
        return {
            "statusCode": 400,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "email, user_name and password are required"}),
        }

    try:
        users_table.put_item(
            Item={"email": email, "user_name": user_name, "password": password},
            ConditionExpression=Attr("email").not_exists(),
        )
    except ClientError as err:
        if err.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return {
                "statusCode": 409,
                "headers": CORS_HEADERS,
                "body": json.dumps({"error": "The email already exists"}),
            }
        raise

    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": json.dumps({"message": "Registered successfully"}),
    }