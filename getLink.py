import boto3
import json

dynamodb = boto3.client("dynamodb")


def lambda_handler(event, context):
    response = dynamodb.get_item(TableName="links", Key={'id': {'S': event['queryStringParameters']['id']}})
    print(response)
    if "Item" in response:

        return {
            'statusCode': 200,
            'body': json.dumps(response["Item"]),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    else:

        return {
            'statusCode': 400,
            'body': json.dumps("User does not exist")}
