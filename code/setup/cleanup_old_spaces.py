# =============================================================================
# COSC2980/2638 Cloud Computing - Assessment 3
# One-off cleanup: removes the old placeholder space_ids that were seeded
# before switching to real RMIT Hanoi Campus room codes.
# =============================================================================

import boto3

from config import AWS_REGION, SPACES_TABLE

OLD_SPACE_IDS = [
    "lib-2f-desk-01", "lib-2f-desk-02", "lib-2f-room-a",
    "lib-3f-desk-01", "lab-3-desk-04", "lab-3-desk-05",
]


def main():
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
    table = dynamodb.Table(SPACES_TABLE)

    for space_id in OLD_SPACE_IDS:
        table.delete_item(Key={"space_id": space_id})
        print(f"Deleted {space_id}")


if __name__ == "__main__":
    main()