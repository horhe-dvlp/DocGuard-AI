FROM nvidia/cuda:13.1.0-runtime-ubuntu24.04

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3-pip \
    wget \
    curl \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libgthread-2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgcc-s1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy and run PaddlePaddle installation script
COPY scripts/install-pp.sh .
RUN chmod +x install-pp.sh && ./install-pp.sh

# Install PaddleOCR after PaddlePaddle
RUN pip3 install --no-cache-dir paddleocr

# Copy application code
COPY app/ ./app/

# Expose port
EXPOSE 8072

# Run the FastAPI application
CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8072"]