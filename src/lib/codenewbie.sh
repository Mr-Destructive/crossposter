#!/bin/usr/env bash

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
export -f codenewbie
