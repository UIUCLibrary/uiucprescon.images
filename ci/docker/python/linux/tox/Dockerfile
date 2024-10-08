ARG PIPX_HOME=/pipx
ARG PIP_DOWNLOAD_CACHE=/.cache/pip
FROM ubuntu:22.04
COPY ci/docker/python/linux/tox/apt-packages.txt /tmp/apt-packages.txt
RUN apt-get update && \
    apt-get install -y software-properties-common gpg-agent --no-install-recommends && \
    add-apt-repository ppa:deadsnakes/ppa && \
    DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata && \
    apt-get update && \
     < /tmp/apt-packages.txt xargs apt-get install -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL

RUN python3.8 -m pip install pip --upgrade && \
    python3.9 -m pip install pip --upgrade && \
    python3.10 -m pip install pip --upgrade && \
    python3.11 -m ensurepip --upgrade && \
    python3.11 -m pip install pip --upgrade

COPY requirements/ /tmp/python_requirements/requirements/
COPY requirements-dev.txt /tmp/python_requirements
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r /tmp/python_requirements/requirements-dev.txt

ARG PIP_DOWNLOAD_CACHE
RUN mkdir -p ${PIP_DOWNLOAD_CACHE} && \
    chmod -R 777 ${PIP_DOWNLOAD_CACHE}
ENV PIP_DOWNLOAD_CACHE=${PIP_DOWNLOAD_CACHE}


ARG PIPX_HOME
ENV PIPX_HOME=${PIPX_HOME}
ENV PIPX_BIN_DIR=${PIPX_HOME}/bin
RUN python3 -m pip install --no-cache-dir pipx && \
    pipx ensurepath && \
    mkdir -p $PIPX_HOME  && chmod -R 777 $PIPX_HOME
RUN PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx install pip-audit

WORKDIR /src
CMD tox --workdir /tmp/tox/  -p=auto --parallel--safe-build --recreate
