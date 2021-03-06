from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from twilio.twiml.voice_response import VoiceResponse

def lambda_handler(event, context):
  
    print(event)

    # Helper class to convert a DynamoDB item to JSON.
    class DecimalEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, decimal.Decimal):
                if o % 1 > 0:
                    return float(o)
                else:
                    return int(o)
            return super(DecimalEncoder, self).default(o)

    dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table('Calls')

    number = event['number']
    time = event['time']

    try:
        response = table.delete_item(
            Key={
                'number': number,
                'time': time
            },
            ReturnValues="ALL_OLD"
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print(response)
        item = response['Attributes']
        print("GetItem succeeded:")
        print(json.dumps(item, indent=4, cls=DecimalEncoder))
        
        # TODO(jmtaber129): Create Twilio markup.
        r = VoiceResponse()
        r.say("It's {0}, {1}!".format(item['caller'], item['excuse']))
        res = {
          "statusCode": 200,
          "headers": {},
          "body": str(r)
        }
        return res
