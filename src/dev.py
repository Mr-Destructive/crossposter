import frontmatter
import requests
import json
import sys
from pathlib import Path

def devto(article):

    with open("keys.txt", "r") as file:
        keys = file.readlines()

    
    with open("config.json", "r") as out:
        config = json.load(out)
    
    output_folder = config["output_folder"]

    output = Path(output_folder)
    output.mkdir(parents=True, exist_ok=True)

    dev_frontmatter = "---\n"
    post = {}
    for key in article:
        post[key] = article[key]
        if key == "body_markdown":
            dev_frontmatter += f"---\n\n{post[key]}"
        else:
            if post[key]:
                if not key == "published":
                    dev_frontmatter += f"{key}: \"{post[key]}\"\n"
                else:
                    dev_frontmatter += f"{key}: {post[key]}\n"
        
    with open(sys.argv[1], "w") as f:
        f.write(dev_frontmatter)

    filename = post['title'].replace(" ", "_").lower()
    output_file = output / f"{filename}_dev_post.md"

    with open(output_file, "w") as file:
        file.write(dev_frontmatter)
        

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
    header={"api-key": dev_keys}
    flag = True
    #author_data = json.loads(requests.get("https://dev.to/api/users/me", headers=header).content)
    #author_username = author_data["username"]
    author_articles_list = json.loads(requests.get("https://dev.to/api/articles/me/published", headers=header).content)
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
