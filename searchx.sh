#!/bin/bash

if [ -f $1.txt ];then less -R $1.txt;
else
for i in "$@" ; do
    if [[ $i == "save" ]] ; then
        ./project.py $1>$1.txt
	less -R $1.text 
        break
    else
	./project.py $1|less -R
    fi
done
fi
