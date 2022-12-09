ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION} as wheel_builder

ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL
ARG PIP_TRUSTED_HOST
ENV PIP_NO_CACHE_DIR=1

ADD requirements.txt ci/docker/shared/requirements-ci.txt ci/docker/shared/requirements-extra.txt /tmp/
COPY requirements/ /tmp/requirements/
RUN python -m pip install --upgrade pip &&  \
    pip install wheel && \
    pip install setuptools --upgrade && \
    pip wheel --wheel-dir=/wheels \
        -r /tmp/requirements.txt \
        -r /tmp/requirements-ci.txt && \
    rm -rf  /root/.cache && \
    pip wheel --wheel-dir=/wheels -r /tmp/requirements-extra.txt

FROM python:${PYTHON_VERSION} as SONAR_BUILDER
RUN apt-get update && \
    apt-get install -y unzip
ENV SONAR_SCANNER_VERSION=4.4.0.2170
ARG SONAR_SCANNER_HOME=/opt/sonar/${SONAR_SCANNER_VERSION}-linux
ENV SONAR_USER_HOME=/opt/sonar/.sonar
RUN curl --create-dirs -sSLo /tmp/sonar-scanner.zip \
        https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-$SONAR_SCANNER_VERSION-linux.zip && \
    unzip -o /tmp/sonar-scanner.zip -d /opt/sonar/ && \
    rm /tmp/sonar-scanner.zip && \
    mkdir -p $SONAR_USER_HOME/cache && \
    chmod -R 777 "${SONAR_USER_HOME}" &&\
    ln -s /opt/sonar/sonar-scanner-$SONAR_SCANNER_VERSION-linux/bin/sonar-scanner /usr/local/bin/sonar-scanner && \
    which sonar-scanner

FROM python:${PYTHON_VERSION}
RUN #apt update && apt install -y libenchant1c2a

COPY --from=SONAR_BUILDER /opt/sonar /opt/sonar/
ENV SONAR_SCANNER_VERSION=4.4.0.2170
ARG SONAR_SCANNER_HOME=/opt/sonar/${SONAR_SCANNER_VERSION}-linux
RUN ln -s /opt/sonar/sonar-scanner-${SONAR_SCANNER_VERSION}-linux/bin/sonar-scanner /usr/local/bin/sonar-scanner && \
    which sonar-scanner
#RUN mkdir -p /home/user/.sonar/ && chmod -R 777 /home/user/

USER root

ENV PIP_FIND_LINKS=/wheels
ENV PIP_NO_CACHE_DIR=1
COPY --from=wheel_builder /wheels /wheels/
ADD requirements.txt ci/docker/shared/requirements-ci.txt /tmp/
COPY requirements/ /tmp/requirements/
RUN pip install --no-index --find-links=/wheels \
    -r /tmp/requirements.txt \
    -r /tmp/requirements-ci.txt
