FROM ubuntu:22.04

# -----------------------
# Instalación del sistema base
# -----------------------
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git wget flex bison gperf python3 python3-pip python3-setuptools python3-venv \
    cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0 \
    build-essential curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# -----------------------
# Variables de entorno
# -----------------------
ENV IDF_PATH=/opt/esp-idf
ENV IDF_TOOLS_PATH=/opt/esp-idf-tools
ENV PATH="$IDF_TOOLS_PATH/tools:$PATH"

# -----------------------
# Clonar ESP-IDF
# -----------------------
RUN mkdir -p ${IDF_PATH} && \
    git clone --recursive https://github.com/espressif/esp-idf.git ${IDF_PATH} && \
    cd ${IDF_PATH} && \
    git checkout release/v5.5 && \
    git pull && \
    git submodule update --init --recursive

# -----------------------
# Instalar dependencias de ESP-IDF
# -----------------------
RUN cd ${IDF_PATH} && ./install.sh


# -----------------------
# Instalar test tools
# -----------------------

RUN . ${IDF_PATH}/export.sh && \
    pip install --no-cache-dir "pytest-embedded-idf[serial]" && \
    pip cache purge


# -----------------------
# Activar entorno por defecto
# -----------------------
RUN echo ". ${IDF_PATH}/export.sh" >> /root/.bashrc

# -----------------------
# Crear punto de entrada para proyectos
# -----------------------
WORKDIR /project

VOLUME ["/project"]

CMD ["/bin/bash"]
