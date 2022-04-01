import requests
import json
import sys


def hashnode(article):
    markdown = sys.argv[1]

    with open("keys.txt", "r") as file:
        keys = file.readlines()

    hashnode_keys = keys[3].split("hashnode:")[1].strip()
    hashnode_id = keys[4].split("hashnode_id:")[1].strip()
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
    # Work in progress
    # data= '{"query":"mutation {
    #    createPublicationStory(
    #        input: {
    #            title: \"'"$title"'\",
    #            contentMarkdown: \"'"$body"'\"
    #            tags: [
    #                {
    #                    _id: \"56744721958ef13879b94ffc\",
    #                    name: \"General Programming\",
    #                    slug: \"programming\"
    #                    }
    #                ]
    #            coverImageURL:\"'"$cover_image"'\"   }
    #            publicationId:\"'"$hash_id"'\",
    #            hideFromHashnodeFeed:false
    #            ) {
    #                message
    #                post{
    #                    title
    #                    coverImage
    #                }
    #            }
    #        }
    #    }' --compressed
    #

    header = {
        "Content-Type": "application/json",
        "Origin": "https://api.hashnode.com",
        "Authorization": hashnode_keys,
    }

    response = requests.post(url=API_ENDPOINT, json={"query": data}, headers=header)

    print("The article URL is:", response.json())
