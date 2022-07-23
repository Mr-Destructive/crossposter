import requests
import json
from crossposter.utils import replace_line


def medium(article, output):

    print("Cross-Posting on medium.com")
    USERNAME_ENDPOINT = "https://api.medium.com/v1/me"

    for line in open("keys.txt", "r"):
        if line.startswith("medium.com:"):
            medium_token = line.split("medium.com:")[1]

    if medium_token != "\n":
        medium_token = medium_token.strip()
    else:
        medium_token = input("Enter the Medium API Token: ")
        replace_line("keys.txt", 1, f"medium.com: {medium_token}\n")

    header = {
        "Authorization": "Bearer " + medium_token,
        "Content-Type": "application/json",
    }

    medium_id = json.loads(requests.get(USERNAME_ENDPOINT, headers=header).content)[
        "data"
    ]["id"]

    API_ENDPOINT = f"https://api.medium.com/v1/users/{medium_id}/posts"

    post = {}
    for key in article:
        post[key] = article[key]

    filename = post["title"].replace(" ", "_").lower()
    output_file = output / f"{filename}_medium_post.md"

    medium_content = ""
    with open(output_file, "w") as f:
        medium_content += f"## {post['title']}\n\n"
        if post["cover_image"]:
            medium_content += (
                f"![{post['title']} 's cover image]({post['cover_image']})\n\n"
            )

        medium_content += post["body_markdown"]

        f.write(medium_content)

    if post["published"] == "true":
        status = "public"
    else:
        status = "draft"

    request_josn = {
        "title": post["title"],
        "contentFormat": "markdown",
        "content": medium_content,
        "publishStatus": status,
    }

    response = requests.post(API_ENDPOINT, headers=header, json=request_josn)

    if response.status_code == 200:
        print("Article Posted at : ", response.content)
    else:
        print(response)
        print(response.content)
