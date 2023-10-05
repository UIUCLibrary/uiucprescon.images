ARG PIP_FIND_LINKS=/wheels
ARG PYTHON_VERSION=3.11

FROM python:${PYTHON_VERSION} as base_image

FROM base_image as wheel_builder
ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL
ARG PIP_TRUSTED_HOST
ENV PIP_NO_CACHE_DIR=1

COPY requirements-ci.txt /requirements/
COPY requirements/ /requirements/requirements/

ARG PIP_FIND_LINKS
RUN mkdir -p ${PIP_FIND_LINKS} &&  \
    pip wheel --wheel-dir=${PIP_FIND_LINKS} --no-cache-dir -r /requirements/requirements-ci.txt

FROM base_image AS SONAR_BUILDER
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

COPY --from=SONAR_BUILDER /opt/sonar /opt/sonar/
ENV SONAR_SCANNER_VERSION=4.4.0.2170
ARG SONAR_SCANNER_HOME=/opt/sonar/${SONAR_SCANNER_VERSION}-linux
RUN ln -s /opt/sonar/sonar-scanner-${SONAR_SCANNER_VERSION}-linux/bin/sonar-scanner /usr/local/bin/sonar-scanner && \
    which sonar-scanner
#RUN mkdir -p /home/user/.sonar/ && chmod -R 777 /home/user/

USER root
ARG PIP_FIND_LINKS
ENV PIP_NO_CACHE_DIR=1
COPY --from=wheel_builder ${PIP_FIND_LINKS} ${PIP_FIND_LINKS}/
COPY --from=wheel_builder requirements/ /requirements
RUN pip install --no-index --find-links=${PIP_FIND_LINKS} \
    -r /requirements/requirements-ci.txt
