#!/bin/usr/env bash

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
