#!/bin/bash

for type in $(ls  | sed 's/.*nophix_fastqc.//' | sort -u | sed 's/.png//')
do
    mkdir --verbose --parents $type
    for file in `find . -name '*'${type}'*'`
    do
        mv -v  $file ${type}/${file}
    done
    cd $type
    montage -verbose -label '%f' \
    -font Helvetica  -pointsize 14 -background 'white' -fill 'black' \
    -define jpeg:size=1600x1600 -geometry 1600x1600+2+2 -auto-orient *.png `basename $PWD`.png
    mv `basename $PWD`.png ../
    rm *.png
    cd -
    rmdir $type
done