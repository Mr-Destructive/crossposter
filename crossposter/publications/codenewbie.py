import requests
import json
from crossposter.utils import hard_to_soft_wraps, replace_line, embeds


def codenewbie_file(article, output):
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


    lines = hard_to_soft_wraps(codenewbie_frontmatter)

    filename = post["title"].replace(" ", "_").lower()
    output_file = output / f"{filename}_codenewbie_post.md"
    with open(output_file, 'w') as f:
        f.writelines(lines)
    print("The Codenewbie frontmatter is generated in the file -> ", output_file)
    return post


def codenewbie(article, output, allow_embeds=False):

    from rich.progress import Progress
    with Progress() as progress:
        task = progress.add_task("Crossposting..",  total=100)
        while not progress.finished:
            progress.update(task, advance=10)

    codenewbie_keys = []
    for line in open("keys.txt", "r"):
        if line.startswith("codenewbie:"):
            codenewbie_keys = line.split("codenewbie:")[1]

    if codenewbie_keys != "\n":
        codenewbie_keys = codenewbie_keys.strip()
    else:
        codenewbie_keys = input("Enter the Codenewbie API Key: ")
        replace_line("keys.txt", 4, f"dev.to: {codenewbie_keys}\n")


    post = codenewbie_file(article, output)

    post = {}

    for key in article:
        post[key] = article[key]

    # replace github and other embed links
    if allow_embeds:
        post = embeds(post)

    API_ENDPOINT = "https://community.codenewbie.org/api/articles"

    data = {
        "Content-Type": "application/json",
        "article": post,
    }
    header = {"api-key": codenewbie_keys}

    flag = True

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

def generate_codenewbie_file(article, output):
    codenewbie_file(article, output)
