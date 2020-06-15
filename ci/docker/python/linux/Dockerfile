ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION} as wheel_builder

ARG CMAKE_DOWNLOAD_URL=https://github.com/Kitware/CMake/releases/download/v3.17.3/cmake-3.17.3-Linux-x86_64.sh
RUN wget -O /tmp/install_cmake.sh $CMAKE_DOWNLOAD_URL
RUN chmod +x /tmp/install_cmake.sh  && /tmp/install_cmake.sh  --skip-license
RUN apt update && apt install -y ninja-build
ADD requirements.txt /tmp/
ARG PYTHON_INDEX=https://devpi.library.illinois.edu/production/release

RUN python -m pip install --upgrade pip &&  \
    pip install setuptools && \
    pip install wheel

RUN pip wheel --wheel-dir=/wheels -r /tmp/requirements.txt -i ${PYTHON_INDEX}

FROM python:${PYTHON_VERSION}
ARG USER_ID=1000
ARG GROUP_ID=1000

RUN groupadd -g $GROUP_ID user && \
    useradd -u $USER_ID -s /bin/sh -m -d /home/user -g user user

COPY --from=wheel_builder /wheels /wheels/
ENV PIP_EXTRA_INDEX_URL="https://devpi.library.illinois.edu/production/release"
ENV PIP_TRUSTED_HOST="devpi.library.illinois.edu"
ENV PIP_FIND_LINKS=/wheels

ADD requirements.txt /tmp/
RUN pip install --no-index --find-links=/wheels \
    -r /tmp/requirements.txt

USER user
WORKDIR /home/user