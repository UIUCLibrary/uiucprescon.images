# escape=`
ARG PYTHON_DOCKER_IMAGE_BASE=python:3.8
FROM ${PYTHON_DOCKER_IMAGE_BASE} as wheel_builder
ARG PIP_INDEX_URL="https://devpi.library.illinois.edu/production/release"
ENV PIP_EXTRA_INDEX_URL="${PIP_INDEX_URL}"
RUN python -m pip install pip --upgrade ; `
    python -m pip install setuptools --upgrade ; `
    python -m pip install wheel

ADD requirements.txt c:/temp/
RUN python -m pip wheel --wheel-dir=c:\temp\wheels `
                        -r c:\temp\requirements.txt

FROM ${PYTHON_DOCKER_IMAGE_BASE}

RUN certutil -generateSSTFromWU roots.sst ; `
    certutil -addstore -f root roots.sst ; `
    del roots.sst

COPY --from=wheel_builder c:\temp\wheels c:\wheels\

ENV PIP_EXTRA_INDEX_URL="${PIP_INDEX_URL}"
ENV PIP_TRUSTED_HOST="devpi.library.illinois.edu"
ENV PIP_FIND_LINKS=c:\wheels\
RUN python -m pip install pip --upgrade ; `
    python -m pip install setuptools --upgrade

ADD requirements.txt c:/temp/
RUN python -m pip install -r c:\temp\requirements.txt