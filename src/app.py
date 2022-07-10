import sys
import frontmatter
from dev import devto
from codenewbie import codenewbie
from hashnode import hashnode
import json

def get_default_or_input(dictionary, keys):
    for key in keys:
        if key in dictionary.keys():
            return dictionary[key]
    return input(f"Enter the {keys[0]} for post: ")
file_markdown = sys.argv[1]

post = frontmatter.load(file_markdown)

with open("config.json", "r") as out:
    config = json.load(out)

blog_link = config["blog_link"]

article = {}
article["title"] = get_default_or_input(post, ["title"])
article["description"] = get_default_or_input(post, ["subtitle", "description"])
slug = get_default_or_input(post, ["slug", "canonical_url"])
image_url = get_default_or_input(post, ["image_url"])
canonical_url = blog_link + str(slug)
article["canonical_url"] = canonical_url
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

if opt == "1":
    devto(article)
elif opt == "2":
    hashnode(article)
elif opt == "3":
    codenewbie(article)
else:
    print("Invalid Option")
