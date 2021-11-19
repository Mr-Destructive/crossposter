#!/usr/bin/env bash

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

sed -i "s/\"/'/g" $file
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

source lib/codenewbie.sh lib/devto.sh lib/medium.sh lib/hashnode.sh

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
