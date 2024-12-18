# Base image
ARG PYTHON_VERSION="3.11"
FROM python:${PYTHON_VERSION}

# Build arguments for dynamic version configuration
ARG PACKMOL_VERSION="20.15.3"

ENV PATH="/opt/tools/packmol-${PACKMOL_VERSION}:$PATH"

# Update and install essential packages
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    gfortran build-essential zip cmake-data cmake curl wget git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


# Install PACKMOL
WORKDIR /opt/tools
RUN wget https://github.com/m3g/packmol/archive/refs/tags/v${PACKMOL_VERSION}.tar.gz && \
    tar -xzvf v${PACKMOL_VERSION}.tar.gz && \
    cd packmol-${PACKMOL_VERSION} && make && \
    rm /opt/tools/v${PACKMOL_VERSION}.tar.gz

# Install IPSuite
WORKDIR /opt/tools/zndraw_utils
COPY ./ ./
RUN pip install .
