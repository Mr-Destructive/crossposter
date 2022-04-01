import requests
import json


def devto(article):

    with open("keys.txt", "r") as file:
        keys = file.readlines()

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
                'body_markdown':article['content']
            },
        }
    """

    response = requests.post(
        url=API_ENDPOINT, json=data, headers={"api-key": dev_keys}
    ).json()
    if "url" in response:
        print("The article URL is: ", response["url"])
    else:
        print("The article URL is: ", response)
