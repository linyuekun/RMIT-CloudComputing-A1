"""
Code adapted from the following links:
https://www.geeksforgeeks.org/how-to-upload-json-file-to-amazon-dynamodb-using-python/
https://www.garysieling.com/blog/uploading-json-files-to-dynamodb-from-python/
"""

import boto3
import json


def load_music(song_list, dynamodb=None):
    if dynamodb is None:
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

    table = dynamodb.Table("music")

    num = 1
    for song in song_list["songs"]:
        title = song["title"]
        artist = song["artist"]
        year = int(song["year"])
        web_url = song["web_url"]
        image_url = song["img_url"]

        print(f" {num}. Adding {title} by {artist} in {year} from {web_url} and {image_url}")
        num += 1

        table.put_item(
            Item={
                "title": title,
                "artist": artist,
                "year": year,
                "web_url": web_url,
                "image_url": image_url
            }
        )


if __name__ == "__main__":
    with open("a1.json") as file:
        data = json.load(file)
    load_music(data)
    print(f"Data loaded successfully!.")
