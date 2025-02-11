#!/bin/bash

DEFAULT_TAG="latest"
TAG="${1:-$DEFAULT_TAG}"

PLATFORM=""
ARCH=$( uname -m )
if [[ ${ARCH} == "arm64" ]]; then
    #	ARCH="x86-64";
    #	PLATFORM="--platform=linux/amd64"
	ARCH="aarch64";
	PLATFORM="--platform=linux/arm64"
fi

# The docker buildx build command
docker buildx build . \
  --file ./Dockerfile \
  --tag "aacic/tiatoolbox:$TAG" \
  $PLATFORM \
  --build-arg ARCH="$ARCH"
