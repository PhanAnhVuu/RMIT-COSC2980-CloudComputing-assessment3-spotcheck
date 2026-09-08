# =============================================================================
# COSC2980/2638 Cloud Computing - Assessment 3
# Creates the Kinesis Data Stream that receives real-time check-in/check-out
# events. Later, a Lambda function will be subscribed to this stream to
# process each event and update DynamoDB.
# =============================================================================

import boto3
from botocore.exceptions import ClientError

from config import AWS_REGION, KINESIS_STREAM


def main():
    kinesis = boto3.client("kinesis", region_name=AWS_REGION)
    try:
        kinesis.create_stream(StreamName=KINESIS_STREAM, ShardCount=1)
        print(f"Creating stream '{KINESIS_STREAM}' ...")
        waiter = kinesis.get_waiter("stream_exists")
        waiter.wait(StreamName=KINESIS_STREAM)
        print(f"Stream '{KINESIS_STREAM}' is ACTIVE.")
    except ClientError as err:
        if err.response["Error"]["Code"] == "ResourceInUseException":
            print(f"Stream '{KINESIS_STREAM}' already exists - reusing it.")
        else:
            raise


if __name__ == "__main__":
    main()