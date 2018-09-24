#!/bin/bash

docker ps -a  | grep Exited   | gawk '{print $1}' | xargs docker rm
docker images | grep '<none>' | gawk '{print $3}' | xargs docker rmi
