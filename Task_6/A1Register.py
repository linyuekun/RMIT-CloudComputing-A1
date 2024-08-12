import boto3
import json

dynamodb = boto3.resource('dynamodb')
login_table = dynamodb.Table('login')

def lambda_handler(event, context):
    request_body = json.loads(event['body'])
    email = request_body['email']
    user_name = request_body['user_name']
    password = request_body['password']


    """
        Code adapted from the following link:
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/put_item.html
    """
    # Store user information in DynamoDB
    login_table.put_item(Item={'email': email, 'user_name': user_name, 'password': password})

    # Return a response
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'User registration successful'})
    }