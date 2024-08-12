import boto3
import json

dynamodb = boto3.resource('dynamodb')
subscriptions_table = dynamodb.Table('subscriptions')

def lambda_handler(event, context):
    request_body = json.loads(event['body'])
    title = request_body['title']
    user_name = request_body['user_name']

    """
        Code adapted from the following link:
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/delete_item.html
    """
    # Delete the subscription from DynamoDB
    subscriptions_table.delete_item(Key={'user_name': user_name, 'title': title})

    # Return a response
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Song unsubscription successful'})
    }