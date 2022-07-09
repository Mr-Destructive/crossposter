from pathlib import Path
import requests
import json
import sys


def hashnode(article):
    markdown = sys.argv[1]

    key_file = Path('keys.txt')
    key_file.touch(exist_ok=True)
    if key_file.is_file():

        f = open(key_file, "r")
        lines = f.readlines()
        print(key_file)
        f = open(key_file, "w")
        lines.append("dev.to:\n")
        lines.append("medium.com:\n")
        lines.append("hashnode:\n")
        lines.append("hashnode_id:\n")
        lines.append("codenewbie:\n")
        f.writelines(lines)
        f.close()
        
    with open(key_file, "r") as file:
        keys = file.readlines()
        print(keys)

    if keys:
        hashnode_keys = keys[2].split("hashnode:")[1].strip()
        hashnode_id = keys[3].split("hashnode_id:")[1].strip()
    else:
        hashnode_keys = input("Enter the hashnode Keys: ")
        hashnode_id = input("Enter your hashnode ID: ")

        f = open(key_file, "r")
        lines = f.readlines()
        lines[2] = "hashnode:" + hashnode_keys + "\n"
        lines[3] = "hashnode_id:" + hashnode_id + "\n"

        f = open(key_file, "w")
        f.writelines(lines)
        f.close()

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
    content = str(content.replace("\"", "\'"))

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
