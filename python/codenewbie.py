import requests
import sys

def codenewbie(article):

    with open('keys.txt', 'r') as file:
        keys = file.readlines()

    codenewbie_keys = keys[5]
    codenewbie_keys = codenewbie_keys.split('codenewbie:')[1].strip()
      
    API_ENDPOINT = "https://community.codenewbie.org/api/articles"
      
    data = {
            'Content-Type': 'application/json',
            'article': {'body_markdown':article},
            }
      
    response = requests.post(url = API_ENDPOINT,json=data, headers={"api-key":codenewbie_keys}).json()
      
    print("The article URL is:", response['url'])

    if(response['url']):
        return True
    return False
