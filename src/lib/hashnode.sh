#!/bin/usr/env bash

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
