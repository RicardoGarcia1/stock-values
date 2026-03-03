import os
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

def get_dynamodb_client(region_name: str = "eu-west-2"):
    boto_config = Config(
        retries={"max_attempts": 10, "mode": "standard"},
        connect_timeout=5,
        read_timeout=5
    )
    if os.getenv("DYNAMO_ENV") == "localstack":
        return boto3.resource(
            "dynamodb",
            endpoint_url=os.getenv("DYNAMO_LOCALSTACK_URL"),
            region_name=region_name,
            config=boto_config
        )
    else: 
        return boto3.resource(
            "dynamodb",
            region_name=region_name,
            config=boto_config
        ) 
          
print("Creating DynamoDB client...")
dynamodb = get_dynamodb_client()


def create_users_table_if_not_exists():
    table_name = "users"
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[{"AttributeName": "user_identifier", "KeyType": "HASH"}],  # Partition Key
            AttributeDefinitions=[{"AttributeName": "user_identifier", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",  # on-demand
        )
        table.wait_until_exists()
        print(f"Tabla '{table_name}' creada correctamente.")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            print(f"La tabla '{table_name}' ya existe.")
        else:
            raise
