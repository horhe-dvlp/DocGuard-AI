FROM nvidia/cuda:13.0.0-runtime-ubuntu22.04

# Add build argument for GPU architecture
ARG GPU_ARCH=120

ENV DEBIAN_FRONTEND=noninteractive
ENV VENV_PATH=/opt/venv
ENV PATH="$VENV_PATH/bin:$PATH"
# Set GPU_ARCH as environment variable
ENV GPU_ARCH=$GPU_ARCH

RUN apt-get update && apt-get install -y python3.10 python3.10-venv python3-pip

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    libglib2.0-0 \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    libgcc-s1 \
    && rm -rf /var/lib/apt/lists/*

RUN python3.10 -m venv $VENV_PATH \
    && $VENV_PATH/bin/pip install --upgrade pip setuptools wheel

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install PaddlePaddle using the script
COPY scripts/install-pp.sh .
RUN chmod +x install-pp.sh && ./install-pp.sh

RUN pip install --no-cache-dir paddleocr[doc-parser]

COPY app/ ./app/

EXPOSE 8072

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8072"]
