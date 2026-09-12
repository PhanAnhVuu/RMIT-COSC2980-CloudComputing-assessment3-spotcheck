# =============================================================================
# COSC2980/2638 Cloud Computing - Assessment 3
# Lambda function: runs Athena queries for historical trends and returns
# the results as JSON.
#
# Triggered by: API Gateway GET /trends
#
# Athena queries are asynchronous: start the query, poll until it finishes,
# then fetch the results - unlike a normal DynamoDB call, which returns
# immediately.
# =============================================================================

import json
import os
import time

import boto3

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
ATHENA_DATABASE = os.environ.get("ATHENA_DATABASE", "spotcheck_db")
ATHENA_OUTPUT = os.environ.get("ATHENA_OUTPUT", "s3://s3926005-spotcheck-floorplans/athena-results/")

athena = boto3.client("athena", region_name=AWS_REGION)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json",
}

QUERIES = {
    "busiest_spaces": """
        SELECT space_id, COUNT(*) AS total_checkins
        FROM checkins
        WHERE status = 'checked_in'
        GROUP BY space_id
        ORDER BY total_checkins DESC
    """,
    "busiest_hours": """
        SELECT hour(from_iso8601_timestamp(event_timestamp)) AS hour_of_day,
               COUNT(*) AS total_checkins
        FROM checkins
        WHERE status = 'checked_in'
        GROUP BY hour(from_iso8601_timestamp(event_timestamp))
        ORDER BY total_checkins DESC
    """,
}


def run_query(sql):
    """Start an Athena query, wait for it to finish, and return the rows."""
    start = athena.start_query_execution(
        QueryString=sql,
        QueryExecutionContext={"Database": ATHENA_DATABASE},
        ResultConfiguration={"OutputLocation": ATHENA_OUTPUT},
    )
    query_id = start["QueryExecutionId"]

    # Poll until the query finishes (Athena queries are asynchronous).
    while True:
        status = athena.get_query_execution(QueryExecutionId=query_id)
        state = status["QueryExecution"]["Status"]["State"]
        if state in ("SUCCEEDED", "FAILED", "CANCELLED"):
            break
        time.sleep(0.5)

    if state != "SUCCEEDED":
        reason = status["QueryExecution"]["Status"].get("StateChangeReason", "unknown error")
        raise RuntimeError(f"Athena query failed: {reason}")

    result = athena.get_query_results(QueryExecutionId=query_id)
    rows = result["ResultSet"]["Rows"]

    # First row is the header; extract column names, then convert the rest.
    columns = [col["VarCharValue"] for col in rows[0]["Data"]]
    data = []
    for row in rows[1:]:
        values = [cell.get("VarCharValue", "") for cell in row["Data"]]
        data.append(dict(zip(columns, values)))
    return data


def lambda_handler(event, context):
    try:
        results = {name: run_query(sql) for name, sql in QUERIES.items()}
    except Exception as exc:
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": str(exc)}),
        }

    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": json.dumps(results),
    }