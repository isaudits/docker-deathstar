#!/bin/bash

docker pull debian
docker build -t deathstar .
docker image prune -f