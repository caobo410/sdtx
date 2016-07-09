#!/bin/bash 

pwd
echo $1
#1.变量定义

do_recursive()
{
    rm *."$1"
    for filename in `ls`
    do
         if [ -d "$filename" ]
         then
             cd $filename
             do_recursive $1
             cd ..
         fi
    done
    return 0
}

do_recursive $1
