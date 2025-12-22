FROM nvidia/cuda:13.0.0-runtime-ubuntu24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV VENV_PATH=/opt/venv
ENV PATH="$VENV_PATH/bin:$PATH"

RUN apt-get update && apt-get install -y \
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


RUN python3 -m venv $VENV_PATH \
    && $VENV_PATH/bin/pip install --upgrade pip setuptools wheel

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY scripts/install-pp.sh .
RUN chmod +x install-pp.sh && ./install-pp.sh


RUN pip install --no-cache-dir paddleocr[doc-parser]


COPY app/ ./app/

EXPOSE 8072

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8072"]
