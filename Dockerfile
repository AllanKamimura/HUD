# ARGUMENTS --------------------------------------------------------------------
##
# Board architecture
##
ARG IMAGE_ARCH=arm64

##
# Base container version
##
ARG BASE_VERSION=3.2.1

##
# Directory of the application inside container
##
ARG APP_ROOT="mpu-test_cv2"

##
# Board GPU vendor prefix
##
ARG GPU="-vivante"


FROM --platform=linux/${IMAGE_ARCH} \
     torizon/qt5-wayland${GPU}:${BASE_VERSION} AS deploy

ARG IMAGE_ARCH
ARG GPU
ARG APP_ROOT

# for vivante GPU we need some "special" sauce
RUN apt-get -q -y update && \
        if [ "${GPU}" = "-vivante" ] || [ "${GPU}" = "-imx8" ]; then \
            apt-get -q -y install \
            imx-gpu-viv-wayland-dev \
        ; else \
            apt-get -q -y install \
            libgl1 \
        ; fi \
    && \
    apt-get clean && apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*

# Install python packages
RUN apt-get -q -y update && \
    apt-get -q -y install \
    python3-minimal \
    python3-pip \
    python3-dev \
    python3-venv \
    python3-pyside2.qtwidgets \
    python3-pyside2.qtgui \
    python3-pyside2.qtqml \
    python3-pyside2.qtcore \
    python3-pyside2.qtquick \
    python3-pyside2.qtnetwork \
    python3-pyside2.qtmultimedia \
    python3-pyside2.qtmultimediawidgets \
    && apt-get clean && apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*

# Install pyqt packages
RUN apt-get -q -y update && \
    apt-get -q -y install \
    qtwayland5 \
    qtmultimedia5-dev \
    qml-module-qtquick-controls \
    qml-module-qtquick-controls2 \
    qml-module-qtquick2 \
    qml-module-qtquick-dialogs \
    qml-module-qtmultimedia \
    libqt5multimedia5-plugins \
    && apt-get clean && apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*

# Install gstream packages
RUN apt-get -y update && apt-get install -y --no-install-recommends libgstreamer1.0-0 \
    gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly gstreamer1.0-tools gstreamer1.0-OpenCV \
    python3-gst-1.0 gstreamer1.0-rtsp libgstrtspserver-1.0-0 gir1.2-gst-rtsp-server-1.0 && \
    apt-get clean && apt-get autoremove && rm -rf /var/lib/apt/lists/*

# Install others packages
RUN apt-get -q -y update && \
    apt-get -q -y install \
    build-essential \
    libcairo2-dev \
    libgirepository1.0-dev \
    v4l-utils \
    rsync \
    nano \
    && apt-get clean && apt-get autoremove && \
    rm -rf /var/lib/apt/lists/*

# Create virtualenv
RUN python3 -m venv ${APP_ROOT}/.venv --system-site-packages

# Install pip packages on venv
COPY requirements-release.txt /requirements-release.txt
RUN . ${APP_ROOT}/.venv/bin/activate && \
    pip3 install --upgrade pip && pip3 install --break-system-packages -r requirements-release.txt && \
    rm requirements-release.txt

USER torizon

# Copy the application source code in the workspace to the $APP_ROOT directory 
# path inside the container, where $APP_ROOT is the torizon_app_root 
# configuration defined in settings.json
COPY ./src ${APP_ROOT}/src

WORKDIR ${APP_ROOT}

ENV APP_ROOT=${APP_ROOT}
ENV QT_QPA_PLATFORM="wayland"
ENV QT_DEBUG_PLUGINS=0
ENV GST_PLUGIN_SCANNER="usr/lib/aarch64-linux-gnu/gstreamer1.0/gstreamer-1.0/gst-plugin-scanner"

# Activate and run the code
CMD . .venv/bin/activate && python3 src/main.py --no-sandbox
