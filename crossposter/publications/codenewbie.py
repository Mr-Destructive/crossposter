import requests
import json
import sys
from crossposter.utils import replace_line


def codenewbie(article, output):

    print("Cross-Posting on codenewbie.community")
    codenewbie_keys = []
    for line in open("keys.txt", "r"):
        if line.startswith("codenewbie:"):
            codenewbie_keys = line.split("codenewbie:")[1]

    if codenewbie_keys != "\n":
        codenewbie_keys = codenewbie_keys.strip()
    else:
        codenewbie_keys = input("Enter the Codenewbie API Key: ")
        replace_line("keys.txt", 4, f"dev.to: {codenewbie_keys}\n")

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

    codenewbie_frontmatter = "---\n"
    post = {}
    for key in article:
        post[key] = article[key]
        if key == "body_markdown":
            codenewbie_frontmatter += f"---\n\n{post[key]}"
        else:
            if post[key]:
                if not key == "published":
                    codenewbie_frontmatter += f'{key}: "{post[key]}"\n'
                else:
                    codenewbie_frontmatter += f"{key}: {post[key]}\n"

    with open(sys.argv[1], "w") as f:
        f.write(codenewbie_frontmatter)

    filename = post["title"].replace(" ", "_").lower()
    output_file = output / f"{filename}_codenewbie_post.md"

    with open(output_file, "w") as file:
        file.write(codenewbie_frontmatter)

    flag = True
    author_articles_list = json.loads(
        requests.get(
            "https://community.codenewbie.org/api/articles/me/published", headers=header
        ).content
    )
    for article_data in author_articles_list:
        if article["body_markdown"] == article_data["body_markdown"]:
            flag = False
            print("ERRR!!!")
            break
        if article["title"] == article_data["title"]:
            flag = False

    if flag:
        response = requests.post(url=API_ENDPOINT, json=data, headers=header).json()
        if "url" in response:
            print("The article URL is: ", response["url"])
        else:
            print("The article URL is: ", response)
    else:
        print("Article already published")
