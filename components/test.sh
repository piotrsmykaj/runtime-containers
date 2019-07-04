#!/bin/sh 

if [ $(getent group wheel) ]
then
	echo "Group exists"
else
	echo "Group doesn't exist"
fi
