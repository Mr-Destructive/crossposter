import requests
import json


def codenewbie(article):

    with open("keys.txt", "r") as file:
        keys = file.readlines()

    codenewbie_keys = keys[4]
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

    API_ENDPOINT = "https://community.codenewbie.org/api/articles"

    data = {
        "Content-Type": "application/json",
        "article": post,
    }
    header = {"api-key": codenewbie_keys}

    flag = True

    author_articles_list = json.loads(requests.get("https://community.codenewbie.org/api/articles/me/published", headers=header).content)
    for article_data in author_articles_list:
        if article["body_markdown"] == article_data["body_markdown"]:
            flag = False
            print("ERRR!!!")
            break
        if article["title"] == article_data["title"]:
            flag = False

    if flag:
        response = requests.post(
            url=API_ENDPOINT, json=data, headers=header
        ).json()
        if "url" in response:
            print("The article URL is: ", response["url"])
        else:
            print("The article URL is: ", response)
    else:
        print("Article already published")
