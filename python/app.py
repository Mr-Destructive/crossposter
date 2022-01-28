import sys
import frontmatter 
import dev
import codenewbie

file_markdown = sys.argv[1]

with open(file_markdown,'r') as file:
    article = file.read()

post=frontmatter.load(file_markdown)

title=post['title']
subtitle=post['subtitle']
canonical_url=post['canonical_url']
cover_image=post['cover_image']
tags=post['tags']
date=post['date']
publishe=post['published']
article=post.content

print(f"1. dev.to \n2. hashnode.com\n3. codenewbie\n4. medium.com\n") 
opt = input("Where you would like to post? (1/2/3/4) : ")

if(opt == '1'):
    dev.devto(article)
elif(opt == '3'):
    codenewbie.codenewbie(article)
else:
    print("Invalid Option")
