"""
Code adapted from the following links:
https://stackoverflow.com/questions/14346065/upload-image-available-at-public-url-to-s3-using-boto
https://erangad.medium.com/upload-a-remote-image-to-s3-without-saving-it-first-with-python-def9c6ee1140
https://theinformationlab.nl/2021/04/30/scripting-file-download-and-upload-to-aws-s3-with-python/
"""

import boto3
import json
import os
import requests
from urllib.parse import urlparse


def download_image(image_url, output_dir):
    try:
        response = requests.get(image_url)
        if response.status_code == 200: # success
            # Extract the filename from the URL
            filename = os.path.basename(urlparse(image_url).path)
            output_path = os.path.join(output_dir, filename)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return output_path
        else:
            print(f"Failed to download image from URL: {image_url}")
    except Exception as e:
        print(f"Error downloading image: {e}")


def upload_to_s3(file_path, bucket_name, s3_key):
    try:
        s3 = boto3.client('s3')
        with open(file_path, 'rb') as f:
            s3.upload_fileobj(f, bucket_name, s3_key)
        print(f"Uploaded {file_path} to S3 bucket {bucket_name} with key {s3_key}")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")


if __name__ == "__main__":
    # Load data from JSON file
    with open("a1.json") as file:
        data = json.load(file)

    # Specify the output directory to save downloaded images
    output_dir = "downloaded_images"
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through each song and download/upload the image
    for song in data['songs']:
        image_url = song['img_url']
        if image_url:
            # Download the image
            downloaded_image_path = download_image(image_url, output_dir)
            if downloaded_image_path:
                # Extract the artist name from the image URL to use as S3 key
                artist_name = urlparse(image_url).path.split('/')[-1].split('.')[0]

                bucket_name = "s3940976-bucket"
                s3_key = f"artist_images/{artist_name}.jpg"
                # Upload the image to S3
                upload_to_s3(downloaded_image_path, bucket_name, s3_key)
