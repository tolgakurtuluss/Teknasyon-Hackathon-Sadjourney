import boto3
import json

dynamodb = boto3.client("dynamodb")
days = ["mo", "tu", "we", "th", "fr", "sa", "su"]


def lambda_handler(event, context):
    response = dynamodb.get_item(TableName="Employee", Key={'id': {'S': event['queryStringParameters']['id']}})

    if "Item" not in response:

        return {
            'statusCode': 400,
            'body': json.dumps('User does not exist')}
    else:
        dynamodb.update_item(
            TableName="Employee",
            Key={'id': {'S': event['queryStringParameters']['id']}},
            UpdateExpression=f"SET {days[int(event['queryStringParameters']['day'])]} = :val",
            ExpressionAttributeValues={':val': {'BOOL': bool(int(event['queryStringParameters']['isAttendance']))}})
        return {
            'statusCode': 200,
            'body': json.dumps("OK")}
