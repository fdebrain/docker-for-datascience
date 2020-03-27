FROM python:3.7-slim

# Install python dependencies
COPY base_requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r base_requirements.txt

# Copy files
COPY base_dashboard.py .

# Expose port to access dashboard
EXPOSE 5006

# Default command when container is run
CMD ["bokeh", "serve", "base_dashboard.py"]