#!/bin/usr/env bash

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
