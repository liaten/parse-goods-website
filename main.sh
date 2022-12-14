#!/bin/bash
rm ./*.{json,jpeg,jpg,png} 2> /dev/null
f=$(echo result.json)
touch $f

if [[ $(bash ./check_geckodriver.sh) == false ]]; then
	wget -O geckodriver.zip https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-win64.zip
	unzip geckodriver.zip
	rm -f geckodriver.zip
	chmod +x geckodriver.exe
fi

if [[ $(bash ./check_ublock.sh) == false ]];then
	wget -O ublock.xpi https://github.com/gorhill/uBlock/releases/download/1.45.3b8/uBlock0_1.45.3b8.firefox.signed.xpi
fi

python ./main.py $1 >> $f
php ./read_file_insert_posts.php