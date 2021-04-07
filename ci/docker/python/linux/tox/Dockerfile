FROM ubuntu:20.04 as wheel_builder_base
COPY ci/docker/python/linux/tox/apt-packages.txt /tmp/apt-packages.txt
RUN apt update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt update && \
    cat /tmp/apt-packages.txt | xargs apt install -y python3-pip

RUN mkdir -p /.cache/pip && \
    chmod -R 777 /.cache

# ******************************************************************************
FROM wheel_builder_base as wheel_builder_py36

RUN apt install -y python3.6-dev python3.6-venv
ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL

COPY requirements.txt ci/docker/shared/requirements-ci.txt ci/docker/shared/requirements-extra.txt  /tmp/
ENV PYTHON=python3.6
RUN $PYTHON -m pip install pip --upgrade pip && \
    $PYTHON -m pip install wheel && \
    $PYTHON -m pip wheel -w /wheels --no-cache-dir \
        -r /tmp/requirements.txt \
        -r /tmp/requirements-ci.txt && \
    $PYTHON -m pip wheel -w /wheels --no-cache-dir -v -r /tmp/requirements-extra.txt

# ==============================================================================
FROM wheel_builder_base as wheel_builder_py37
RUN apt install -y python3.7-dev python3.7-venv

ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL
COPY requirements.txt ci/docker/shared/requirements-ci.txt ci/docker/shared/requirements-extra.txt  /tmp/
ENV PYTHON=python3.7
RUN $PYTHON -m pip install pip --upgrade pip && \
    $PYTHON -m pip install wheel && \
    $PYTHON -m pip wheel -w /wheels --no-cache-dir \
        -r /tmp/requirements.txt \
        -r /tmp/requirements-ci.txt && \
    $PYTHON -m pip wheel -w /wheels --no-cache-dir -v -r /tmp/requirements-extra.txt

# ==============================================================================
FROM wheel_builder_base as wheel_builder_py38
RUN apt install -y python3.8-dev python3.8-venv

ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL

COPY requirements.txt ci/docker/shared/requirements-ci.txt ci/docker/shared/requirements-extra.txt  /tmp/
ENV PYTHON=python3.8
RUN $PYTHON -m pip install pip --upgrade pip && \
    $PYTHON -m pip install wheel && \
    $PYTHON -m pip wheel -w /wheels --no-cache-dir \
        -r /tmp/requirements.txt \
        -r /tmp/requirements-ci.txt && \
    $PYTHON -m pip wheel -w /wheels --no-cache-dir -v -r /tmp/requirements-extra.txt

# ==============================================================================
FROM wheel_builder_base as wheel_builder_py39
RUN apt install -y python3.9-dev python3.9-venv

ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL

COPY requirements.txt ci/docker/shared/requirements-ci.txt ci/docker/shared/requirements-extra.txt  /tmp/
ENV PYTHON=python3.9
RUN $PYTHON -m pip install pip --upgrade pip && \
    $PYTHON -m pip install wheel && \
    $PYTHON -m pip wheel -w /wheels --no-cache-dir \
        -r /tmp/requirements.txt \
        -r /tmp/requirements-ci.txt && \
    $PYTHON -m pip wheel -w /wheels --no-cache-dir -v -r /tmp/requirements-extra.txt

# ==============================================================================

FROM wheel_builder_base

ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL

COPY --from=wheel_builder_py36 /wheels/* /wheels/
RUN python3.6 -m pip install pip --upgrade
COPY --from=wheel_builder_py37 /wheels/* /wheels/
RUN python3.7 -m pip install pip --upgrade
COPY --from=wheel_builder_py38 /wheels/* /wheels/
RUN python3.8 -m pip install pip --upgrade
COPY --from=wheel_builder_py39 /wheels/* /wheels/
RUN python3.9 -m pip install pip --upgrade

RUN chmod -R 777 /wheels
ENV PIP_FIND_LINKS=/wheels
RUN pip3 install tox devpi_client build && \
    python3 -m build -h

WORKDIR /src
CMD tox --workdir /tmp/tox/  -p=auto --parallel--safe-build --recreate