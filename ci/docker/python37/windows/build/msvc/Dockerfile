# escape=`
ARG PYTHON_DOCKER_IMAGE_BASE=python:3.7
FROM ${PYTHON_DOCKER_IMAGE_BASE} as builder

ENV PIP_DOWNLOAD_CACHE=c:\pip_cache `
    PIP_EXTRA_INDEX_URL="https://devpi.library.illinois.edu/production/release" `
    PIP_TRUSTED_HOST="devpi.library.illinois.edu"

RUN python -m pip install pip --upgrade ; `
        pip install --extra-index-url https://devpi.library.illinois.edu/production/release `
        --trusted-host devpi.library.illinois.edu `
        pipenv `
        pylint

ENV PIPENV_CACHE_DIR=c:\pipenv_cache `
    WORKON_HOME=c:\venvs `
    PIPENV_NOSPIN=True

ADD Pipfile Pipfile.lock c:\temp\
RUN cd c:\temp\ ; pipenv install --dev --extra-index-url https://devpi.library.illinois.edu/production/release --verbose ; pipenv run pip freeze > requirements.txt

FROM ${PYTHON_DOCKER_IMAGE_BASE}
RUN mkdir temp
COPY --from=builder c:/temp/requirements.txt c:/temp/requirements.txt
ENV PIP_EXTRA_INDEX_URL="https://devpi.library.illinois.edu/production/release"
ENV PIP_TRUSTED_HOST="devpi.library.illinois.edu"

RUN python -m pip install --upgrade pip ; pip install -r c:/temp/requirements.txt
RUN certutil -generateSSTFromWU roots.sst ; `
    certutil -addstore -f root roots.sst ; `
    del roots.sst