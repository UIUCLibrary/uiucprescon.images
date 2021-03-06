ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION} as wheel_builder

ARG CMAKE_DOWNLOAD_URL=https://github.com/Kitware/CMake/releases/download/v3.17.3/cmake-3.17.3-Linux-x86_64.sh
RUN wget -O /tmp/install_cmake.sh $CMAKE_DOWNLOAD_URL && \
    chmod +x /tmp/install_cmake.sh  && /tmp/install_cmake.sh  --skip-license && \
    cmake --version

RUN apt update && apt install -y ninja-build
ARG PIP_INDEX_URL=https://devpi.library.illinois.edu/production/release
ARG PIP_EXTRA_INDEX_URL
ARG PIP_TRUSTED_HOST
ENV PIP_NO_CACHE_DIR=1

ADD requirements.txt ci/docker/shared/requirements-ci.txt ci/docker/shared/requirements-extra.txt /tmp/
RUN python -m pip install --upgrade pip &&  \
    pip install wheel && \
    pip install setuptools --upgrade && \
    pip wheel --wheel-dir=/wheels \
        -r /tmp/requirements.txt \
        -r /tmp/requirements-ci.txt && \
    rm -rf  /root/.cache && \
    pip wheel --wheel-dir=/wheels -r /tmp/requirements-extra.txt

FROM python:${PYTHON_VERSION}
RUN apt update && apt install -y libenchant1c2a
ARG USER_ID=1000
ARG GROUP_ID=1000

RUN groupadd -g $GROUP_ID user && \
    useradd -u $USER_ID -s /bin/sh -m -d /home/user -g user user && \
    mkdir -p /.cache/pip && chgrp -R  user /.cache/ && \
    chmod -R g+w /.cache/

USER user
ENV SONAR_SCANNER_VERSION=4.4.0.2170
ENV SONAR_SCANNER_HOME=/home/user/.sonar/sonar-scanner-$SONAR_SCANNER_VERSION-linux
RUN curl --create-dirs -sSLo $HOME/.sonar/sonar-scanner.zip \
        https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-$SONAR_SCANNER_VERSION-linux.zip && \
    unzip -o $HOME/.sonar/sonar-scanner.zip -d $HOME/.sonar/ && \
    rm $HOME/.sonar/sonar-scanner.zip && \
    mkdir -p /home/user/.sonar/cache && \
    chown user:user /home/user/.sonar/cache
ENV PATH=$SONAR_SCANNER_HOME/bin:$PATH
ENV SONAR_SCANNER_OPTS="-server"

USER root

ENV PIP_FIND_LINKS=/wheels
ENV PIP_NO_CACHE_DIR=1
COPY --from=wheel_builder /wheels /wheels/
ADD requirements.txt ci/docker/shared/requirements-ci.txt /tmp/
RUN pip install --no-index --find-links=/wheels \
    -r /tmp/requirements.txt \
    -r /tmp/requirements-ci.txt

USER user
WORKDIR /home/user