# escape=`
ARG PYTHON_DOCKER_IMAGE_BASE=python:3.8
FROM ${PYTHON_DOCKER_IMAGE_BASE} as wheel_builder
ARG PIP_INDEX_URL=https://devpi.library.illinois.edu/production/release
ARG PIP_EXTRA_INDEX_URL
ARG PIP_TRUSTED_HOST
ENV PIP_NO_CACHE_DIR=1
ADD requirements.txt ci/docker/shared/requirements-ci.txt ci/docker/shared/requirements-extra.txt c:/temp/
RUN python -m pip install pip --upgrade ; `
    python -m pip install setuptools --upgrade ; `
    python -m pip install wheel ; `
    python -m pip wheel --wheel-dir=c:\temp\wheels `
                        -r c:\temp\requirements.txt `
                        -r c:\temp\requirements-ci.txt ; `
    pip wheel --wheel-dir=c:\temp\wheels `
                        -r c:\temp\requirements-extra.txt

FROM ${PYTHON_DOCKER_IMAGE_BASE}

RUN certutil -generateSSTFromWU roots.sst ; `
    certutil -addstore -f root roots.sst ; `
    del roots.sst

ARG PIP_INDEX_URL=https://devpi.library.illinois.edu/production/release
ARG PIP_EXTRA_INDEX_URL
ARG PIP_TRUSTED_HOST
ENV PIP_NO_CACHE_DIR=1

COPY --from=wheel_builder c:\temp\wheels c:\wheels\

ADD requirements.txt ci/docker/shared/requirements-ci.txt c:/temp/
RUN python -m pip install pip --upgrade ; `
    python -m pip install setuptools --upgrade ; `
    python -m pip install --no-index --find-links=c:\wheels\ `
        -r c:\temp\requirements.txt `
        -r c:\temp\requirements-ci.txt

ENV PIP_FIND_LINKS=c:\wheels\