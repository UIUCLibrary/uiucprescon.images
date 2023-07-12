ARG PIP_DOWNLOAD_CACHE=/.cache/pip
FROM ubuntu:20.04
COPY ci/docker/python/linux/tox/apt-packages.txt /tmp/apt-packages.txt
RUN apt update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt update && \
    cat /tmp/apt-packages.txt | xargs apt install -y python3-pip

RUN mkdir -p /.cache/pip && \
    chmod -R 777 /.cache

ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL

RUN python3.8 -m pip install pip --upgrade && \
    python3.9 -m pip install pip --upgrade && \
    python3.10 -m ensurepip --upgrade && \
    python3.10 -m pip install pip --upgrade

COPY requirements /tmp/requirements
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install wheel && \
    python3 -m pip wheel -w /wheels --no-cache-dir wheel && \
    python3 -m pip install -r /tmp/requirements/requirements_tox.txt devpi-client build && \
    python3 -m build -h

ARG PIP_DOWNLOAD_CACHE
RUN mkdir -p ${PIP_DOWNLOAD_CACHE} && \
    chmod -R 777 ${PIP_DOWNLOAD_CACHE}
ENV PIP_DOWNLOAD_CACHE=${PIP_DOWNLOAD_CACHE}

WORKDIR /src
CMD tox --workdir /tmp/tox/  -p=auto --parallel--safe-build --recreate
