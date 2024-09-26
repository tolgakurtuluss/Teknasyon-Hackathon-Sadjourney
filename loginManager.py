import boto3
import json

dynamodb = boto3.client("dynamodb")


def lambda_handler(event, context):
    response = dynamodb.get_item(TableName="Driver" if int(event['queryStringParameters']['isDriver']) else "Employee",
                                 Key={'id': {'S': event['queryStringParameters']['id']}})

    if "Item" in response:
        if response["Item"]["password"]["S"] == event['queryStringParameters']['password']:
            return {
                'statusCode': 200,
                'body': json.dumps("OK")}

        else:
            return {
                'statusCode': 400,
                'body': json.dumps("Incorrect password")}

    else:
        return {
            'statusCode': 400,
            'body': json.dumps("User does not exist")}
