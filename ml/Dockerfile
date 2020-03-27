FROM fdebrain/base_docker_datascience:1.0

# Install python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy files
COPY dashboard.py .

# Expose port to access dashboard
EXPOSE 5006

# Default command when container is run
CMD ["bokeh", "serve", "dashboard.py"]