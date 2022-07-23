from pathlib import Path
import requests
import json
import sys


def hashnode(article, output):
    markdown = sys.argv[1]

    for line in open("keys.txt", "r"):
        if line.startswith("hashnode:"):
            hashnode_keys = line.split("hashnode:")[1]
        if line.startswith("hashnode_id:"):
            hashnode_id = line.split("hashnode_id:")[1]

    if hashnode_keys != "\n":
        hashnode_keys = hashnode_keys.strip()
    else:
        hashnode_keys = input("Enter the Hashnode API Key: ")
        replace_line("keys.txt", 2, f"hashnode: {hashnode_keys}\n")
    if hashnode_id != "\n":
        hashnode_id = hashnode_id.strip()
    else:
        hashnode_id = input("Enter your Hashnode ID: ")
        replace_line("keys.txt", 3, f"hashnode_id: {hashnode_id}\n")

    title = str(article["title"])
    subtitle = article["description"]
    canonical_url = article["canonical_url"]
    cover_image = article["cover_image"]
    tags = article["tags"]
    published = article["published"]
    content = article["body_markdown"].replace(
        "\n", "\\n"
    )  # .replace("\\c", "\c").replace("\r",  "\t")
    content = "".join(content.splitlines())
    content = str(content.replace('"', "'"))

    API_ENDPOINT = "https://api.hashnode.com"

    data = f"""
    mutation{{
       createPublicationStory(
           input: {{
               title: "{title}"
               contentMarkdown: "{content}",
               tags: [
                   {{
                       _id: "56744721958ef13879b94ffc",
                       name: "General Programming",
                       slug: "programming",
                   }}
               ]
               coverImageURL:"{cover_image}" 
                  }}
               publicationId: "{hashnode_id}",
               hideFromHashnodeFeed:false
               ) {{
                   message
                   post{{
                       title
                   }}
               }}
           }}"""

    header = {
        "Content-Type": "application/json",
        "Origin": "https://api.hashnode.com",
        "Authorization": hashnode_keys,
    }

    response = requests.post(url=API_ENDPOINT, json={"query": data}, headers=header)

    print("The article URL is:", response.json())
