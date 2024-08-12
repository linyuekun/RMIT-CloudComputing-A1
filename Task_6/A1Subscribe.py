import boto3
import json

dynamodb = boto3.resource('dynamodb')
subscriptions_table = dynamodb.Table('subscriptions')

def lambda_handler(event, context):
    request_body = json.loads(event['body'])
    title = request_body['title']
    artist = request_body['artist']
    year = request_body['year']
    user_name = request_body['user_name']

    # Store subscription information in DynamoDB
    subscriptions_table.put_item(Item={'user_name': user_name, 'title': title, 'artist': artist, 'year': year})

    # Return a response
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Song subscription successful'})
    }
