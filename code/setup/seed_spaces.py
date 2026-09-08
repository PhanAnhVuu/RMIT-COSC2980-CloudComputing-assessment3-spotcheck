# =============================================================================
# COSC2980/2638 Cloud Computing - Assessment 3
# Seeds the "spaces" table with sample study spaces.
# =============================================================================

import boto3

from config import AWS_REGION, SPACES_TABLE

SAMPLE_SPACES = [
    {"space_id": "lib-2f-desk-01", "name": "Library 2F Desk 1", "floor": "2", "building": "Library", "capacity": 1},
    {"space_id": "lib-2f-desk-02", "name": "Library 2F Desk 2", "floor": "2", "building": "Library", "capacity": 1},
    {"space_id": "lib-2f-room-a", "name": "Library 2F Group Room A", "floor": "2", "building": "Library", "capacity": 6},
    {"space_id": "lib-3f-desk-01", "name": "Library 3F Desk 1", "floor": "3", "building": "Library", "capacity": 1},
    {"space_id": "lab-3-desk-04", "name": "Lab 3 Desk 4", "floor": "1", "building": "Building 14", "capacity": 1},
    {"space_id": "lab-3-desk-05", "name": "Lab 3 Desk 5", "floor": "1", "building": "Building 14", "capacity": 1},
]


def main():
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
    table = dynamodb.Table(SPACES_TABLE)

    with table.batch_writer() as batch:
        for space in SAMPLE_SPACES:
            batch.put_item(Item=space)

    print(f"Loaded {len(SAMPLE_SPACES)} spaces into '{SPACES_TABLE}'.")


if __name__ == "__main__":
    main()