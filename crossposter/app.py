import sys
import json
import frontmatter
import argparse
from rich import print
from pathlib import Path
from .publications.dev import devto
from .publications.codenewbie import codenewbie
from .publications.hashnode import hashnode
from .publications.medium import medium


def get_default_or_input(dictionary, keys):
    for key in keys:
        if key in dictionary.keys():
            return dictionary[key]
    return input(f"Enter the {keys[0]} for post: ")


def main():
    print("[bold green]Crossposter[/ bold green]")
    if len(sys.argv) < 2:
        file_markdown = input("Enter the filename: ")
    else:
        file_markdown = sys.argv[1]

    while not file_markdown:
        print(f"No File Found with name {file_markdown}!")
        file_markdown = input("Enter the filename: ")
        if file_markdown:
            if Path(file_markdown).exists():
                break
            else:
                continue

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "Path",
        metavar="path",
        type=str,
        nargs="?",
        const=1,
        default=file_markdown,
        help="the path to file",
    )
    parser.add_argument("--dev", action="store_true", help="Post to dev.to")
    parser.add_argument("--med", action="store_true", help="Post to medium.com")
    parser.add_argument("--cdb", action="store_true", help="Post to codenewbie")
    args = parser.parse_args()
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
    # while True:
    #    if validators.url(slug):
    #        break
    #    else:
    #        slug = input("Enter a valid URL: ")

    if "slug" in post:
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

    key_file = Path("keys.txt")
    if not key_file.exists():
        key_file.touch(exist_ok=True)
        with open(key_file, "r+") as f:
            lines = f.readlines()
            lines.append("dev.to:\n")
            lines.append("medium.com:\n")
            lines.append("hashnode:\n")
            lines.append("hashnode_id:\n")
            lines.append("codenewbie:\n")
            f.writelines(lines)

    if args.dev:
        devto(article, output)
    elif args.med:
        medium(article, output)
    elif args.cdb:
        codenewbie(article, output)
    else:
        print(f"1. dev.to \n2. hashnode.com\n3. codenewbie\n4. medium.com\n")
        opt = input("Where you would like to post? (1/2/3/4) : ")
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
