FROM fdebrain/base_docker_datascience:1.0

# Install OpenCV runtime dependencies
# https://github.com/NVIDIA/nvidia-docker/issues/864#issuecomment-452023152
# https://stackoverflow.com/a/60221324
RUN apt-get update && \
    apt-get -y install libglib2.0 libsm6 libxext6 libxrender-dev && \
    apt-get clean

# Install python packages
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy files
COPY templates ./templates
COPY data ./data
COPY camera.py dashboard.py ./

EXPOSE 5006

# Default command when container is run
CMD ["python", "dashboard.py"]