import requests
import sys

def devto(article):
    with open('keys.txt', 'r') as file:
        keys = file.readlines()

    dev_keys = keys[0]
    dev_keys = dev_keys.split('dev.to:')[1].strip()
      
    API_ENDPOINT = "https://dev.to/api/articles"
      
    data = {
            'Content-Type': 'application/json',
            'article': {'body_markdown':article},
            }
      
    response = requests.post(url = API_ENDPOINT,json=data, headers={"api-key":dev_keys}).json()
      
    print("The article URL is: ",response['url'])
    if(response['url']):
        return True
    return False
