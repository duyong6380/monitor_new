#!/bin/bash

ftp_user="afteam"
ftp_passwd="afteam"
ftp_src_url="200.200.155.143/bugreport/bug/"
ftp_login=""
ftp_reconnect_times=10 #ftp文件传输重连次数

#从ftp上获取数据文件
get_files()
{
	ftp_url=$ftp_src_url`date +%Y%m%d`
	echo $ftp_url
    ftp_login="ftp://$ftp_user:$ftp_passwd@$ftp_url/*" 
    echo $ftp_login

    wget -q -c -t $ftp_reconnect_times -r $ftp_login
    if [ $? -ne 0 ];then
        exit 1
    fi
}

echo "begin get_files:"
get_files
echo "finish get_files:"


