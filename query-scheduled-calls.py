from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime
from twilio.rest import Client

print('Loading Function')

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

    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('Calls')

    curr_time = int(datetime.today().timestamp())
    print(curr_time)
    
    fe = Key('time').lte(curr_time)
    
    response = table.scan(
        FilterExpression=fe
    )    
    
    account_sid = 'ID'
    auth_token = 'TOKEN'
    client = Client(account_sid, auth_token)

    for i in response['Items']:
        url_call = 'https://o76jou3rti.execute-api.us-west-2.amazonaws.com/prod/TwilioCallback?' \
        + 'number=' + str(i['number']) + '&time=' + str(i['time'])
    
        call = client.calls.create(to=i[number],
                                   from_="+18179853304",
                                   method='GET',
                                   url=url_call)
    print(call.sid)
    
    

if (__name__ == '__main__'):
    lambda_handler({}, {})
