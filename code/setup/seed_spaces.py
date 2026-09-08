# =============================================================================
# COSC2980/2638 Cloud Computing - Assessment 3
# Seeds the "spaces" table with sample study spaces from RMIT Hanoi Campus.
# =============================================================================

import boto3

from config import AWS_REGION, SPACES_TABLE

SAMPLE_SPACES = [
    {"space_id": "1-1-309", "name": "Student Centre", "floor": "1", "building": "Hanoi Campus", "capacity": 10, "floorplan_key": "floorplans/level-1.jpg"},
    {"space_id": "1-1-006", "name": "International Office", "floor": "1", "building": "Hanoi Campus", "capacity": 4, "floorplan_key": "floorplans/level-1.jpg"},
    {"space_id": "1-1-008", "name": "Meeting Room (Level 1)", "floor": "1", "building": "Hanoi Campus", "capacity": 6, "floorplan_key": "floorplans/level-1.jpg"},
    {"space_id": "1-2-006", "name": "Library Study Area", "floor": "2", "building": "Hanoi Campus", "capacity": 20, "floorplan_key": "floorplans/level-2.jpg"},
    {"space_id": "1-2-010", "name": "Library Guest Room", "floor": "2", "building": "Hanoi Campus", "capacity": 4, "floorplan_key": "floorplans/level-2.jpg"},
    {"space_id": "1-2-013", "name": "Meeting Room (Library)", "floor": "2", "building": "Hanoi Campus", "capacity": 6, "floorplan_key": "floorplans/level-2.jpg"},
    {"space_id": "1-2-001", "name": "Student Access Lab", "floor": "2", "building": "Hanoi Campus", "capacity": 15, "floorplan_key": "floorplans/level-2.jpg"},
    {"space_id": "1-2-016", "name": "Mac Lab", "floor": "2", "building": "Hanoi Campus", "capacity": 12, "floorplan_key": "floorplans/level-2.jpg"},
    {"space_id": "1-10-001", "name": "Lab Room (SBM)", "floor": "10", "building": "Hanoi Campus", "capacity": 10, "floorplan_key": "floorplans/level-3.jpg"},
    {"space_id": "1-10-002", "name": "Lab Room (SCD)", "floor": "10", "building": "Hanoi Campus", "capacity": 10, "floorplan_key": "floorplans/level-3.jpg"},
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