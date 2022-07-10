import sys
import frontmatter
from pathlib import Path
from .publications.dev import devto
from .publications.codenewbie import codenewbie
from .publications.hashnode import hashnode
from .publications.medium import medium
import json


def get_default_or_input(dictionary, keys):
    for key in keys:
        if key in dictionary.keys():
            return dictionary[key]
    return input(f"Enter the {keys[0]} for post: ")


def main():
    file_markdown = sys.argv[1]

    post = frontmatter.load(file_markdown)

    with open("config.json", "r") as out:
        config = json.load(out)

    output_folder = config["output_folder"]

    output = Path(output_folder)
    output.mkdir(parents=True, exist_ok=True)

    blog_link = config["blog_link"]

    article = {}
    article["title"] = get_default_or_input(post, ["title"])
    article["description"] = get_default_or_input(post, ["subtitle", "description"])
    slug = get_default_or_input(post, ["slug", "canonical_url"])
    if post["slug"]:
        slug = blog_link + str(slug)
    image_url = get_default_or_input(post, ["image_url", "cover_image"])

    article["canonical_url"] = slug
    article["cover_image"] = image_url
    article["tags"] = get_default_or_input(post, ["tags"])
    # article['date']=post['date']
    status = get_default_or_input(post, ["status", "published"])
    if status == "published":
        article["published"] = "true"
    else:
        article["published"] = "false"
    article["body_markdown"] = post.content
    if "series" in post:
        article["series"] = post["series"]

    print(f"1. dev.to \n2. hashnode.com\n3. codenewbie\n4. medium.com\n")
    opt = input("Where you would like to post? (1/2/3/4) : ")

    key_file = Path("keys.txt")
    key_file.touch(exist_ok=True)
    if key_file.is_file():

        f = open(key_file, "r")
        lines = f.readlines()
        f = open(key_file, "w")
        lines.append("dev.to:\n")
        lines.append("medium.com:\n")
        lines.append("hashnode:\n")
        lines.append("hashnode_id:\n")
        lines.append("codenewbie:\n")
        f.writelines(lines)
        f.close()

    if opt == "1":
        devto(article, output)
    elif opt == "2":
        hashnode(article, output)
    elif opt == "3":
        codenewbie(article, output)
    elif opt == "4":
        medium(article, output)
    else:
        print("Invalid Option")


if __name__ == "__main__":
    main()
