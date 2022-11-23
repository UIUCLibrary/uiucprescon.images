FROM ubuntu:20.04 as wheel_builder_base
COPY ci/docker/python/linux/tox/apt-packages.txt /tmp/apt-packages.txt
RUN apt update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt update && \
    cat /tmp/apt-packages.txt | xargs apt install -y python3-pip

RUN mkdir -p /.cache/pip && \
    chmod -R 777 /.cache


# ==============================================================================
FROM wheel_builder_base as wheel_builder_py37

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
FROM wheel_builder_base as wheel_builder_py310

ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL

COPY requirements.txt ci/docker/shared/requirements-ci.txt ci/docker/shared/requirements-extra.txt  /tmp/
ENV PYTHON=python3.10
RUN $PYTHON -m ensurepip --upgrade && \
    $PYTHON -m pip install pip --upgrade pip && \
    $PYTHON -m pip install wheel && \
    $PYTHON -m pip wheel -w /wheels --no-cache-dir \
        -r /tmp/requirements.txt \
        -r /tmp/requirements-ci.txt && \
    $PYTHON -m pip wheel -w /wheels --no-cache-dir -v -r /tmp/requirements-extra.txt

# ==============================================================================

FROM wheel_builder_base

ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL

COPY --from=wheel_builder_py37 /wheels/* /wheels/
RUN python3.7 -m pip install pip --upgrade

COPY --from=wheel_builder_py38 /wheels/* /wheels/
RUN python3.8 -m pip install pip --upgrade

COPY --from=wheel_builder_py39 /wheels/* /wheels/
RUN python3.9 -m pip install pip --upgrade

COPY --from=wheel_builder_py310 /wheels/* /wheels/
RUN python3.10 -m ensurepip --upgrade && \
    python3.10 -m pip install pip --upgrade

RUN chmod -R 777 /wheels
ENV PIP_FIND_LINKS=/wheels
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install wheel && \
    python3 -m pip wheel -w /wheels --no-cache-dir wheel && \
    python3 -m pip install tox "devpi-client<6.0" build && \
    python3 -m build -h

WORKDIR /src
CMD tox --workdir /tmp/tox/  -p=auto --parallel--safe-build --recreate