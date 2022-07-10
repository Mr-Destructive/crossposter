import requests
import json

def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    print(lines)
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

def medium(article, output):

    USERNAME_ENDPOINT = "https://api.medium.com/v1/me"
    with open('keys.txt', 'r') as f:
        keys = f.readlines()

    if len(keys[2].split("medium.com"))>1:
        medium_token = keys[2].split("medium.com:")[1].strip()
    else:
        medium_token = input("Enter your medium token: ")
        replace_line("keys.txt", 2, f"medium.com:{medium_token}\n")
        

    header = {"Authorization": "Bearer " + medium_token, "Content-Type": "application/json"}

    medium_id = json.loads(requests.get(USERNAME_ENDPOINT, headers=header).content)["data"]["id"]

    API_ENDPOINT = f"https://api.medium.com/v1/users/{medium_id}/posts"

    post = {}
    for key in article:
        post[key] = article[key]

    filename = post['title'].replace(" ", "_").lower()
    output_file = output / f"{filename}_medium_post.md"

    medium_content = ""
    with open(output_file, "w") as f:
        medium_content += f"## {post['title']}\n\n"
        if post["cover_image"]:
            medium_content += f"![{post['title']} 's cover image]({post['cover_image']})\n\n"

        medium_content+= post["body_markdown"]

        f.write(medium_content)

    if post["published"] == "true":
        status="public"
    else:
        status="draft"
        

    request_josn = {"title": post["title"], "contentFormat": "markdown", "content": medium_content, "publishStatus": status}

    response = requests.post(API_ENDPOINT, headers=header, json=request_josn)

    if response.status_code == 200:
        print("Article Posted at : ", response.content)
    else:
        print(response)
        print(response.content)
