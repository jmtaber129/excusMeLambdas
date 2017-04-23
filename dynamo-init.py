from __future__ import print_function # Python 2/3 compatibility
import boto3

print('Loading function')

def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")


    table = dynamodb.create_table(
        TableName='Calls',
        KeySchema=[
            {
                'AttributeName': 'datetime',
                'KeyType': 'HASH'  #Sort key
            },
            {
                'AttributeName': 'number',
                'KeyType': 'RANGE'  #Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'number',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'datetime',
                'AttributeType': 'N'
            }

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    print("Table status:", table.table_status)

if (__name__ == '__main__'):
    lambda_handler({}, {})
