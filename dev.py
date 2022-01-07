import requests

with open('m.md','r') as file:
    countriesStr = file.read()

with open('keys.txt', 'r') as file:
    keys = file.readlines()

dev_keys = keys[0]
dev_keys = dev_keys.split('dev.to:')[1].strip()
  
API_ENDPOINT = "https://dev.to/api/articles"
  
source_code = countriesStr
  
data = {
        'Content-Type': 'application/json',
        'article': {'body_markdown':source_code},
        }
  
response = requests.post(url = API_ENDPOINT,json=data, headers={"api-key":dev_keys}).json()
  
print("The article URL-id is:%s"%response.get("id"),response.get("created_at"))
