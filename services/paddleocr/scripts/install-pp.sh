#!/bin/bash

set -e

echo "Detecting GPU architecture..."

# get GPU architecture function
get_gpu_arch() {
    # Check if GPU_ARCH is set as environment variable (for Docker build)
    if [[ -n "$GPU_ARCH" ]]; then
        echo "$GPU_ARCH"
        return
    fi
    
    if command -v nvidia-smi &> /dev/null; then
        local compute_cap=$(nvidia-smi --query-gpu=compute_cap --format=csv,noheader,nounits | head -n1 | tr -d ' ')
        if [[ -n "$compute_cap" ]]; then
            local major=$(echo $compute_cap | cut -d'.' -f1)
            local minor=$(echo $compute_cap | cut -d'.' -f2)
            echo $((major * 10 + minor))
        else
            echo "0"
        fi
    else
        echo "0"
    fi
}

# GPU architecture detection
DETECTED_GPU_ARCH=$(get_gpu_arch)

echo "Detected GPU architecture: sm_$DETECTED_GPU_ARCH"

# PaddlePaddle installation based on GPU architecture
if [[ "$DETECTED_GPU_ARCH" == "120" ]]; then
    echo "Installing custom PaddlePaddle for sm_120 architecture..."
    pip3 install --no-cache-dir https://github.com/horhe-dvlp/paddlepaddle-sm120-wheels/releases/download/v3.3.0-dev-sm120/paddlepaddle_gpu-3.3.0.dev20251209-cp310-cp310-linux_x86_64.whl
elif [[ "$DETECTED_GPU_ARCH" -gt "0" ]]; then
    echo "Installing standard PaddlePaddle GPU version..."
    pip3 install --no-cache-dir paddlepaddle-gpu
else
    echo "No GPU detected, installing CPU version..."
    pip3 install --no-cache-dir paddlepaddle
fi

echo "PaddlePaddle installation completed!"