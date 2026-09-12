# =============================================================================
# COSC2980/2638 Cloud Computing - Assessment 3
# Creates the three DynamoDB tables SpotCheck needs.
#
# users     - partition key: email (String)
# spaces    - partition key: space_id (String)
# checkins  - partition key: space_id (String), sort key: timestamp (String)
# =============================================================================

import boto3
from botocore.exceptions import ClientError

from config import AWS_REGION, USERS_TABLE, SPACES_TABLE, CHECKINS_TABLE, ACTIVITY_TABLE


def create_table_if_missing(dynamodb, table_name, key_schema, attribute_defs):
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_defs,
            BillingMode="PAY_PER_REQUEST",
        )
        print(f"Creating table '{table_name}' ...")
        table.wait_until_exists()
        print(f"Table '{table_name}' is ACTIVE.")
    except ClientError as err:
        if err.response["Error"]["Code"] == "ResourceInUseException":
            print(f"Table '{table_name}' already exists - reusing it.")
        else:
            raise


def main():
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)

    create_table_if_missing(
        dynamodb, USERS_TABLE,
        key_schema=[{"AttributeName": "email", "KeyType": "HASH"}],
        attribute_defs=[{"AttributeName": "email", "AttributeType": "S"}],
    )

    create_table_if_missing(
        dynamodb, SPACES_TABLE,
        key_schema=[{"AttributeName": "space_id", "KeyType": "HASH"}],
        attribute_defs=[{"AttributeName": "space_id", "AttributeType": "S"}],
    )

    create_table_if_missing(
        dynamodb, CHECKINS_TABLE,
        key_schema=[
            {"AttributeName": "space_id", "KeyType": "HASH"},
            {"AttributeName": "timestamp", "KeyType": "RANGE"},
        ],
        attribute_defs=[
            {"AttributeName": "space_id", "AttributeType": "S"},
            {"AttributeName": "timestamp", "AttributeType": "S"},
        ],
    )

    create_table_if_missing(
        dynamodb, ACTIVITY_TABLE,
        key_schema=[
            {"AttributeName": "space_id", "KeyType": "HASH"},
            {"AttributeName": "date", "KeyType": "RANGE"},
        ],
        attribute_defs=[
            {"AttributeName": "space_id", "AttributeType": "S"},
            {"AttributeName": "date", "AttributeType": "S"},
        ],
    )


if __name__ == "__main__":
    main()