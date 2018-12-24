#!/bin/bash

docker pull debian:stable
docker build -t isaudits/deathstar .
docker image prune -f