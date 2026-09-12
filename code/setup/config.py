# =============================================================================
# COSC2980/2638 Cloud Computing - Assessment 3
# SpotCheck - Shared configuration for setup scripts and Lambda functions.
# =============================================================================

import os

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

USERS_TABLE = os.environ.get("USERS_TABLE", "spotcheck_users")
SPACES_TABLE = os.environ.get("SPACES_TABLE", "spotcheck_spaces")
CHECKINS_TABLE = os.environ.get("CHECKINS_TABLE", "spotcheck_checkins")

# S3 bucket for floor plan images. Bucket names must be globally unique.
STUDENT_ID = os.environ.get("STUDENT_ID", "s3926005")
S3_BUCKET = os.environ.get("S3_BUCKET", f"{STUDENT_ID}-spotcheck-floorplans")

# Kinesis stream that receives check-in/check-out events in real time.
KINESIS_STREAM = os.environ.get("KINESIS_STREAM", "spotcheck-events")
ACTIVITY_TABLE = os.environ.get("ACTIVITY_TABLE", "spotcheck_activity_counts")