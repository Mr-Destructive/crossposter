import requests
import sys

markdown = sys.argv[1]
with open(markdown,'r') as file:
    article = file.read()

with open('keys.txt', 'r') as file:
    keys = file.readlines()

hashnode_keys = keys[4]
hashnode_keys = hashnode_keys.split('hashnode:')[1].strip()
  
API_ENDPOINT = "https://api.hashnode.com"
  
# Work in progress
#data= '{"query":"mutation {
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
#header = {
#    'Accept-Encoding': 'gzip, deflate',
#    'Content-Type': 'application/json',
#    'Accept': 'application/json',
#    'Connection': 'keep-alive', 
#    'DNT': '1' 
#    'Origin': 'https://api.hashnode.com'
#    'Authorization': hashnode_keys, 
#        }
#  
#response = requests.post(url = API_ENDPOINT,json=data, headers=header.json())
#  
#print("The article URL is:", response['url'])

