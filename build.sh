#!/bin/bash

docker pull debian:stable
docker build -t deathstar .
docker image prune -f