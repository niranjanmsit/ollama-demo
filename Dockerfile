FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml ./
COPY *.py ./

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Default command
CMD ["python", "main.py"]

