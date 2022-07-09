import sys
import frontmatter
from dev import devto
from codenewbie import codenewbie
from hashnode import hashnode

file_markdown = sys.argv[1]

post = frontmatter.load(file_markdown)

article = {}
if any(key in post for key in ["description", "subtitle"]):
    article["description"] = post.get("subtitle", "description")
article["title"] = post["title"]
article["description"] = post["subtitle"]
slug = post.get("slug", "")
image_url = post.get("image_url", "")
canonical_url = "https://www.meetgor.com/" + slug
article["canonical_url"] = canonical_url
article["cover_image"] = image_url
article["tags"] = post["tags"]
# article['date']=post['date']
article["published"] = post["status"]
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
