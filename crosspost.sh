#!/usr/bin/env bash

function dev()
{
    if [[ -z $(sed -n -e 's/.*dev.to://p' $keys) ]];then
        read -p "Enter the dev.to API key : " dev_key
        sed -i "/dev.to:/ s/$/$dev_key/" $keys
    fi

    curl -s -X POST -H "Content-Type: application/json" \
      -H "api-key: $dev_key" -d "{\"article\":{\"body_markdown\":\"$body\"}}" \
      https://dev.to/api/articles

    if [[ $? ]];then 
        echo -e "\nPosted on dev.to\n"
    else
        echo -e "Error...\nFailed to post on dev.to"
    fi

}

function hashnode()
{

    if [[ -z $(sed -n -e 's/.*hashnode://p' $keys ) ]]; then
        read -p "Enter the hashnode.com token : " hashtoken
        sed -i "/hashnode:/ s/$/$hashtoken/" $keys
    fi

    if [[ -z $(sed -n -e 's/.*node_id://p' $keys ) ]]; then
        read -p "Enter the hashnode username : " hash_uname
        curl -s 'https://api.hashnode.com/' -H 'Accept-Encoding: gzip, deflate, br' -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Connection: keep-alive' -H 'DNT: 1' -H 'Origin: https://api.hashnode.com' -H 'Authorization: \"'"$hash_token"'\"' --data-binary '{"query":"query user {\n  user(username: \"'"$hash_uname"'\") {\n    publication {\n      _id\n    }\n  }\n}\n"}' --compressed >temp.json
        hash_id=$(grep -o -P '(?<=id":").*(?=")' temp.json)
        sed -i "/hashnode_id:/ s/$/$hash_id/" $keys
    fi

    cat $file | sed '1,9{/^---/!{/^\---/!d}}' | sed '1,2d' >temp.txt
    cat temp.txt | awk '{print $0" "}' >temp.txt
    sed -i '/^- / s/$/\\r\\n/g' temp.txt
    sed -i '/^[0-9]. / s/$/\\r\\n/' temp.txt
    sed 's/$/\\r\\n\\r\\n/g' temp.txt >temp.md
    cat temp.md | tr -d '\r\n' | sed 's/\\r\\n/<br>/g' >body.md
    body=$(cat body.md)
    
    # comment out the below two lines for non-publication posts
    #curl 'https://api.hashnode.com/' -H 'Accept-Encoding: gzip, deflate, br' -H 'Content-Type: application/json' -H 'Accept: application/json'\
    #    -H 'Connection: keep-alive' -H 'DNT: 1' -H 'Origin: https://api.hashnode.com' -H 'Authorization: '$hash_token'' --data-binary '{"query":"mutation {\n  createStory(\n    input: {\n      title: \"'"$title"'\",\n      contentMarkdown: \"'"$body"'\"\n      tags: [\n        {\n          _id: \"56744721958ef13879b94ff1\",\n          name: \"General Programming\",\n          slug: \"programming\"\n        }\n      ]\n    }\n     ) {\n    message\n    post{\n      title\n    }\n  }\n}\n\n "}' --compressed

    curl -s 'https://api.hashnode.com/' -H 'Accept-Encoding: gzip, deflate, br' -H 'Content-Type: application/json' -H 'Accept: application/json'\
        -H 'Connection: keep-alive' -H 'DNT: 1' -H 'Origin: https://api.hashnode.com' -H 'Authorization: '$hashtoken'' --data-binary '{"query":"mutation {\n  createPublicationStory(\n    input: {\n      title: \"'"$title"'\",\n      contentMarkdown: \"'"$body"'\"\n      tags: [\n        {\n          _id: \"56744721958ef13879b94ffc\",\n          name: \"General Programming\",\n          slug: \"programming\"\n        }\n      ]\n coverImageURL:\"'"$cover_image"'\"   }\n    publicationId:\"'"$hash_id"'\",\n    hideFromHashnodeFeed:false\n  ) {\n    message\n    post{\n      title\ncoverImage\n    }\n  }\n}\n"}' --compressed

    if [[ $? ]];then 
        echo -e "\nPosted on hashnode.com\n"
    else
        echo -e "Error...\nFailed to post on hashnode.com"
    fi

}

function medium()
{

    if [[ -z $(sed -n -e 's/.*ium://p' $keys ) ]]; then
        read -p "Enter the medium.com API token : " med_token
        med_id=$(curl -s -H "Authorization: Bearer $med_token" https://api.medium.com/v1/me | json_pp >temp.json)
        med_id=$(grep -o -P '(?<=id).*(?=,)' temp.json )
        med_id=$(echo ${med_id:3} | tr -d '"')
        sed -i "/medium:/ s/$/$med_token/" $keys
        sed -i "/medium_id:/ s/$/$med_id/" $keys
    fi

    tags=$(echo $tags | sed "s/ //g")
    tags=$(echo $tags | sed "s/,/','/g" | sed "s/$/'/" | sed "s/^/'/" | sed "s/\b\(.\)/\u\1/g")
    if [[ $statusp = "true" ]];then
        mstatus="public"
    else
        mstatus="draft"
    fi

    awk '{print $0" "}' $file >temp.txt
    cat temp.txt | sed '1,10{/^---/!{/^\---/!d}}' | sed '1,2d' >temp.txt
	sed -i "1a # $title\\r\\n" temp.txt	
	sed -i "2a $subtitle\\r\\n" temp.txt	
	sed -i "2a ![]($cover_image)" temp.txt
    
    sed -i '/^- / s/$/\\r\\n/g' temp.txt
    sed -i '/^[0-9]. / s/$/\\r\\n/' temp.txt
    awk '!NF{$0="\\r\\n\\r\\n"}1' temp.txt >temp.md
	cat temp.md | tr -d '\r\n' > body.md
	body=$(cat body.md)

    curl -s -H "Authorization: Bearer $med_token " -H "Content-Type: application/json" \
        -H "Accept: application/json" -H "Accept-Charset: utf-8" --request "POST" \
        -d '{ "title": "'"$title"'", "contentFormat": "markdown", "content": "'"$body"'", "canonicalUrl": "'"$canonical_url"'", "tags": ["'"$tags"'"],"publishStatus": "'"$mstatus"'" }'\
        "https://api.medium.com/v1/users/$med_id/posts"

    if [[ $? ]];then 
        echo -e "\nPosted on medium.com\n"
    else
        echo -e "Error...\nFailed to post on medium.com"
    fi

}

function codenewbie()
{
    if [[ -z $(sed -n -e 's/.*codenewbie://p' $keys) ]];then
        read -p "Enter the codenewbie API key : " codenbkeys
        sed -i "/codenewbie:/ s/$/$codenbkeys/" $keys
    fi

	curl  -X POST -H "Content-Type: application/json" \
	  -H "api-key: $codenbkeys" \
	  -d '{"article":{"body_markdown":"'"$body"'"}}' \
	  https://community.codenewbie.org/api/articles
    echo $?
    if [[ $? ]];then 
        echo -e "\nPosted on codenewbie\n"
    else
        echo -e "Error...\nFailed to post on dev.to"
    fi
}

touch keys.txt body.md temp.md temp.txt
keys=keys.txt

if [[ ! -s $keys ]];then
    head -n 1 $keys | echo "dev.to:" >$keys
    sed -i "1a medium:" $keys
    sed -i "2a medium_id:" $keys
    sed -i "3a hashnode:" $keys
    sed -i "4a hashnode_id:" $keys
    sed -i "5a codenewbie:" $keys
else
    dev_key=$(sed -n -e 's/dev.to://p' $keys)
    med_token=$(sed -n -e 's/medium://p' $keys)
    med_id=$(sed -n -e 's/medium_id://p' $keys)
    hashtoken=$(sed -n -e 's/hashnode://p' $keys)
    hash_id=$(sed -n -e 's/hashnode_id://p' $keys)
    codenbkeys=$(sed -n -e 's/codenewbie://p' $keys)
fi

read -p "Enter the name of the file : " file

if [[ -z $(sed '/^---/p;q' $file) ]];then
    read -p "Enter the title of your post : " title
    read -p "Enter the subtitle of your post : " subtitle
    read -p "Enter the status of your post(true/false) : " statusp
    read -p "Enter the tags for your post    : " tags
    read -p "Enter the canonical url of the post   : " canonical_url
    read -p "Enter the cover_image url of the post : " cover_image
    read -p "Should this be a part of a series? (y/n) : " series_bool

    if [[ $series_bool = "y" || $series_bool = "Y" ]]; then
        read -p "Enter the name of the series : " series
    fi

    sed -i "1i ---" $file  
    sed -i "1a title: $title" $file
    sed -i "2a subtitle: $subtitle" $file
    sed -i "3a published: $statusp" $file
    sed -i "4a tags: $tags" $file
    sed -i "5a canonical_url: $canonical_url" $file
    sed -i "6a cover_image: $cover_image" $file
    sed -i "7a series: $series" $file
    sed -i "8a ---" $file
fi

title=$(sed -n '2 s/^[^=]*title: *//p' $file)
subtitle=$(sed -n '3 s/^[^=]*subtitle: *//p' $file)
tags=$(sed -n '5 s/^[^=]*tags: *//p' $file)
canonical_url=$(sed -n '6 s/^[^=]*url: *//p' $file)
cover_image=$(sed -n '7 s/^[^=]*age: *//p' $file)

awk '{print $0" "}' $file >temp.txt
sed -i '1,+7 s/$/\\r\\n/g' temp.txt
sed -i '/^- / s/$/\\r\\n/g' temp.txt
sed -i '/^[0-9]. / s/$/\\r\\n/' temp.txt
awk '!NF{$0="\\r\\n\\r\\n"}1' temp.txt >temp.md
cat temp.md | tr -d '\r\n' >body.md
body=$(cat body.md)


echo -e "\n1. dev.to \n"
echo -e "2. hashnode.com \n"
echo -e "3. medium.com \n"
echo -e "4. All of the above\n"
echo -e "5. dev.to and medium\n"
echo -e "6. codenewbie \n"

read -p "Where you want to cross post to? " num

if [[ $num -eq 1 ]];then

    dev

elif [[ $num -eq 2 ]];then

    hashnode

elif [[ $num -eq 3 ]];then

    medium

elif [[ $num -eq 4 ]];then

    dev
    hashnode
    medium

elif [[ $num -eq 5 ]];then

    dev
    medium

elif [[ $num -eq 6 ]];then

    codenewbie

else
	echo "Invalid Input"	
fi

rm temp.md temp.txt body.md
