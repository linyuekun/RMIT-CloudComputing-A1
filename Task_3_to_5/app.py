"""
Code adapted from the following link:
https://www.linkedin.com/learning/flask-essential-training/web-development-with-flask?u=91782594
"""

from flask import Flask, render_template, request, redirect, url_for, session
import boto3
from boto3.dynamodb.conditions import Attr, Key
import requests

app = Flask(__name__)
# Set a secret key for session management
app.secret_key = 's3940976'

# Define the URLs of API endpoints for lambda functions
REGISTER_ENDPOINT = "https://xt8fg1tt04.execute-api.us-east-1.amazonaws.com/default/A1Register"
SUBSCRIBE_ENDPOINT = "https://f6xc0pbtog.execute-api.us-east-1.amazonaws.com/default/A1Subscribe"
UNSUBSCRIBE_ENDPOINT = "https://a89hewekvl.execute-api.us-east-1.amazonaws.com/default/A1Unsubscribe"

# Initialize AWS DynamoDB clients
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
login_table_name = 'login'
login_table = dynamodb.Table(login_table_name)
music_table_name = 'music'
music_table = dynamodb.Table(music_table_name)
subscriptions_table_name = 'subscriptions'
subscriptions_table = dynamodb.Table(subscriptions_table_name)

# Connect to AWS S3
s3 = boto3.client('s3', region_name='us-east-1')
bucket_name = 's3940976-bucket'


# Function to generate presigned URL for an image
def generate_presigned_url(object_key):
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket_name,
            'Key': object_key
        },
        # Set expiration to 1 hour
        ExpiresIn=3600
    )
    return url


"""
Code adapted from the following links:
https://stackoverflow.com/questions/62047167/show-image-stored-in-s3-on-web-page-using-flask
https://www.twilio.com/en-us/blog/media-file-storage-python-flask-amazon-s3-buckets
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
"""


# Function to retrieve image URL from S3
def get_image_url(artist_name):
    # Specify the sub-folder to retrieve the image
    # Also trim artist name to match image name
    # Have to adjust some image name later in AWS S3
    object_key = 'artist_images/' + artist_name.replace(' ', '') + '.jpg'
    presigned_url = generate_presigned_url(object_key)
    return presigned_url


# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if user exists in DynamoDB
        response = login_table.get_item(Key={'email': email})
        if 'Item' in response:
            stored_password = response['Item']['password']
            if password == stored_password:
                # Store user_name in session
                session['user_name'] = response['Item']['user_name']
                return redirect(url_for('main'))

        # Display error message if email or password is invalid
        error = "Email or password is invalid!"
        return render_template('login.html', error=error)

    return render_template('login.html')


# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        user_name = request.form['user_name']
        password = request.form['password']

        # Check if email already exists in DynamoDB
        response = login_table.get_item(Key={'email': email})
        if 'Item' in response:
            # Display error message if email is invalid
            error = 'The email already exists!'
            return render_template('register.html', error=error)

        # If email doesn't exist, add to DynamoDB
        # Make a POST request to the API endpoint for running lambda function to register
        registration_details = {
            'email': email,
            'user_name': user_name,
            'password': password
        }
        response = requests.post(REGISTER_ENDPOINT, json=registration_details)

        # Return to login page if successful
        if response.status_code == 200:
            return redirect(url_for('login'))

    return render_template('register.html')


# Logout route
@app.route('/logout')
def logout():
    # remove session for user_name and return to login page
    session.pop('user_name', None)
    return redirect(url_for('login'))


# Main route
@app.route('/main', methods=['GET', 'POST'])
def main():
    # Initiate a session for user_name
    user_name = session['user_name']
    # Initiate a blank variable to be used to filter out search
    subscribed_titles = []

    if request.method == 'POST':
        # If logout
        if request.form.get('logout'):
            logout()

        title = request.form.get('title')
        artist = request.form.get('artist')
        year = request.form.get('year')

        """
        Code adapted from the following link:
        https://iamvickyav.medium.com/aws-dynamodb-with-python-boto3-part-3-query-items-from-dynamodb-f99e62a34227
        """
        # Set condition for each field
        # If it strings, we can look for partial letters, but case-sensitive
        # The number has to be exact
        filter_expression = None
        if title:
            filter_expression = Attr('title').contains(title)
        if artist:
            filter_expression = filter_expression & Attr('artist').contains(artist) if filter_expression else Attr(
                'artist').contains(artist)
        if year:
            filter_expression = filter_expression & Key('year').eq(int(year)) if filter_expression else Key('year').eq(
                int(year))

        # Check with DynamoDB for matching information
        if filter_expression:
            response = music_table.scan(FilterExpression=filter_expression)
            items = response['Items']
            if not items:
                # Error message once there is no match
                query_result = "No result is retrieved. Please query again."
            else:
                for item in items:
                    # if found, initiate image_url from artist name and append it to the result
                    item['image_url'] = get_image_url(item['artist'])
                query_result = items

                # Check for songs already subscribed using user_name
                # This is used to filter out search result
                response = subscriptions_table.scan(FilterExpression=Attr('user_name').eq(user_name))
                subscriptions = response['Items']
                subscribed_titles = [subscription['title'] for subscription in subscriptions]

        else:
            # Error message when query without input
            query_result = "Please enter at least one query condition!"

        # Check for user's subscriptions using user_name
        response = subscriptions_table.scan(FilterExpression=Attr('user_name').eq(user_name))
        subscriptions = response['Items']

        # Update the image URLs for subscriptions
        for subscription in subscriptions:
            subscription['image_url'] = get_image_url(subscription['artist'])
        return render_template('main.html', user_name=user_name, query_result=query_result, subscriptions=subscriptions, subscribed_titles=subscribed_titles)

    # Check for user's subscriptions using user_name
    # This is used to show all subscriptions
    response = subscriptions_table.scan(FilterExpression=Attr('user_name').eq(user_name))
    subscriptions = response['Items']

    # Update the image URLs for subscriptions
    for subscription in subscriptions:
        subscription['image_url'] = get_image_url(subscription['artist'])

    return render_template('main.html', user_name=user_name, subscriptions=subscriptions)


# Subscribe route
@app.route('/subscribe', methods=['POST'])
def subscribe():
    if 'user_name' not in session:
        return redirect(url_for('login'))

    title = request.form.get('title')
    artist = request.form.get('artist')
    year = request.form.get('year')
    user_name = session['user_name']

    # Add subscription information in DynamoDB
    # Make a POST request to the API endpoint for running lambda function to subscribe
    subscription_details = {
        'user_name': user_name,
        'title': title,
        'artist': artist,
        'year': year
    }
    response = requests.post(SUBSCRIBE_ENDPOINT, json=subscription_details)

    # Refresh the main page
    if response.status_code == 200:
        return redirect(url_for('main'))


# Remove subscription route
@app.route('/remove', methods=['POST'])
def remove():
    if 'user_name' not in session:
        return redirect(url_for('login'))

    title = request.form.get('title')
    user_name = session['user_name']

    # Delete subscription from DynamoDB
    # Make a POST request to the API endpoint for running lambda function to unsubscribe
    unsubscription_details = {
        'user_name': user_name,
        'title': title,
    }
    response = requests.post(UNSUBSCRIBE_ENDPOINT, json=unsubscription_details)

    # Refresh the main page
    if response.status_code == 200:
        return redirect(url_for('main'))

    return redirect(url_for('main'))


if __name__ == "__main__":
    app.run(debug=True)
