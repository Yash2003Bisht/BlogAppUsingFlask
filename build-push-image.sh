#!/bin/bash

printf "Please enter the image version: " "$VERSION"
read VERSION

# remove the existing image
docker remove ghcr.io/blog-site-docker/blog-site:"$VERSION"

# build the image
docker buildx build -t ghcr.io/blog-site-docker/blog-site:"$VERSION" .

# push the image
docker push ghcr.io/blog-site-docker/blog-site:"$VERSION"
