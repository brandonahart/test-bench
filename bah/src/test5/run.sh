#!/usr/bin/env sh

docker run --rm -it -p 9000:8000 --entrypoint bash debian:loader-dev
