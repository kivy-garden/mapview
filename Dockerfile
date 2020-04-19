# Docker image for installing dependencies on Linux and running tests.
# Build with:
# docker build --tag=mapview-linux .
# Run with:
# docker run mapview-linux /bin/sh -c 'tox'
# Or for interactive shell:
# docker run -it --rm mapview-linux
# For using the UI from Docker you may need to:
# xhost +local:
FROM ubuntu:18.04

# install system dependencies
RUN apt -y update -qq > /dev/null && apt install --yes --no-install-recommends \
    build-essential \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    pkg-config \
	python3-pip \
	python3-setuptools \
    tox \
    && python3 -m pip install --upgrade --no-cache setuptools \
    && apt -y autoremove \
    && apt -y clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
