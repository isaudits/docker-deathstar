#!/bin/bash

if [[ $(uname -s) == Linux ]]
then
    docker run -it --rm --net=host isaudits/deathstar "$@"
else
    #NOTE - we should also map 137-138:137-138/udp but OSX has netbiosd running on those ports...
    
    docker run -it --rm \
    -p 21:21 -p 25:25 -p 53:53 -p 80:80 -p 88:88 -p 110:110 -p 135:135 -p 143:143 -p 389:389 -p 443:443 -p 445:445 -p 587:587 -p 3141:3141 -p 8443:8443 \
    -p 53:53/udp -p 88:88/udp -p 1434:1434/udp \
    isaudits/deathstar "$@"
fi
