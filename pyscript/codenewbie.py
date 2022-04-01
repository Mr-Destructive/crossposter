import requests
import json
import sys


def codenewbie(article):

    with open("keys.txt", "r") as file:
        keys = file.readlines()

    codenewbie_keys = keys[5]
    codenewbie_keys = codenewbie_keys.split("codenewbie:")[1].strip()

    API_ENDPOINT = "https://community.codenewbie.org/api/articles"

    """
    data = {
            'Content-Type': 'application/json',
            'article': {
                'title': article['title'],
                'description': article['subtitle'],
                'canonical_url': article['canonical_url'],
                'published': article['published'],
                'tags': article['tags'],
                'series': article['series'],
                'cover_image': article['cover_image'],
                'body_markdown': article['content']
            },
        }
    """

    post = {}

    for key in article:
        post[key] = article[key]

    dev_keys = keys[0]
    dev_keys = dev_keys.split("dev.to:")[1].strip()

    API_ENDPOINT = "https://dev.to/api/articles"

    data = {
        "Content-Type": "application/json",
        "article": post,
    }
    print(data)
    header = {"api-key": codenewbie_keys}
    response = requests.post(
        url=API_ENDPOINT, json=data, headers={"api-key": codenewbie_keys}
    ).json()

    print("The article URL is:", response)
