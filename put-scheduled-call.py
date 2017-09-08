from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from datetime import datetime

print('Loading function')

def lambda_handler(event, context):

    # Helper class to convert a DynamoDB item to JSON.
    class DecimalEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, decimal.Decimal):
                if o % 1 > 0:
                    return float(o)
                else:
                    return int(o)
            return super(DecimalEncoder, self).default(o)

    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Calls')

    number = int(event['number'])
    time = int(datetime.today().timestamp() + (int(event['delay']) * 60))
    print(time)
    caller = event['caller']
    excuse = event['excuse']
    

    response = table.put_item(
       Item={
            'number': number,
            'time': time,
            'caller': caller,
            'excuse': excuse
        }
    )
    
    print("PutItem succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))
    
    status = response['ResponseMetadata']['HTTPStatusCode']
    if (status == 200):
        return True
    return False

if (__name__ == '__main__'):
  event = {
    'number': 6824297206,
    'delay': 5,
    'caller': 'Dad',
    'excuse': 'Your apartment is flooded'
  }
  result = lambda_handler(event, {})
  print(result)
