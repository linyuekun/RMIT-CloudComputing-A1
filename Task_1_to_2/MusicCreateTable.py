"""
Code adapted from the following link:
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.client.run-application-python.01-create-table.html
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
"""

import boto3


def create_music_table(dynamodb=None):
    if dynamodb is None:
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")  # Specify "us-east-1" as region

    table_name = "music"
    params = {
        "TableName": table_name,
        "KeySchema": [
            {"AttributeName": "title", "KeyType": "HASH"}  # Partition key
        ],
        "AttributeDefinitions": [
            {"AttributeName": "title", "AttributeType": "S"},  # String
        ],
        "ProvisionedThroughput": {"ReadCapacityUnits": 10, "WriteCapacityUnits": 10}
    }

    table = dynamodb.create_table(**params)
    print(f"Creating {table_name}")
    table.wait_until_exists()

    return table


if __name__ == "__main__":
    music_table = create_music_table()
    print(f"Table created successfully!.")
