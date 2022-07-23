import requests
import json
from crossposter.utils import hard_to_soft_wraps, replace_line


def devto(article, output):

    print("Cross-Posting on dev.to")
    dev_keys = []
    for line in open("keys.txt", "r"):
        if line.startswith("dev.to:"):
            dev_keys = line.split("dev.to:")[1]

    if dev_keys != "\n":
        dev_keys = dev_keys.strip()
    else:
        dev_keys = input("Enter the DEV API Key: ")
        replace_line("keys.txt", 0, f"dev.to: {dev_keys}\n")

    dev_frontmatter = "---\n"
    post = {}
    for key in article:
        post[key] = article[key]
        if key == "body_markdown":
            dev_frontmatter += f"---\n\n{post[key]}"
        else:
            if post[key]:
                if not key == "published":
                    dev_frontmatter += f'{key}: "{post[key]}"\n'
                else:
                    dev_frontmatter += f"{key}: {post[key]}\n"

    filename = post["title"].replace(" ", "_").lower()
    output_file = output / f"{filename}_dev_post.md"

    import re

    lines = hard_to_soft_wraps(dev_frontmatter)

    with open(output_file, "w") as f:
        f.writelines(lines)
    print("The DEV frontmatter is generated in the file -> ", output_file)

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
    header = {"api-key": dev_keys}
    flag = True
    # author_data = json.loads(requests.get("https://dev.to/api/users/me", headers=header).content)
    # author_username = author_data["username"]
    author_articles_list = json.loads(
        requests.get("https://dev.to/api/articles/me/published", headers=header).content
    )
    for article_data in author_articles_list:
        if article["body_markdown"] == article_data["body_markdown"]:
            flag = False
            print("ERRR!!!")
            break
        if article["title"] == article_data["title"]:
            flag = False

    if flag:
        response = requests.post(
            url=API_ENDPOINT, json=data, headers={"api-key": dev_keys}
        ).json()
        if "url" in response:
            print("The article URL is: ", response["url"])
        else:
            print("The article URL is: ", response)
    else:
        print("Article already published")
