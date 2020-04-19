# Docker image for installing dependencies on Linux and running tests.
# Build with:
# docker build --tag=mapview-linux .
# Run with:
# docker run mapview-linux /bin/sh -c 'tox'
# Or for interactive shell:
# docker run -it --rm mapview-linux
FROM ubuntu:18.04

# configure locale
RUN apt -y update -qq > /dev/null && apt install --yes --no-install-recommends \
    locales \
    && locale-gen en_US.UTF-8 \
    && apt -y autoremove \
    && apt -y clean \
    && rm -rf /var/lib/apt/lists/*
ENV LANG="en_US.UTF-8" \
    LANGUAGE="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8"

# install system dependencies
RUN apt -y update -qq > /dev/null && apt install --yes --no-install-recommends \
    build-essential \
    git \
    lsb-release \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libssl-dev \
    make \
    pkg-config \
	python3-pip \
	python3-setuptools \
    tox \
    virtualenv \
    && python3 -m pip install --upgrade --no-cache setuptools \
    && apt -y autoremove \
    && apt -y clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
