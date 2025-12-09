# Use a slim Python image
FROM python:3.10-slim

WORKDIR /app

# Install gcc (needed for some python libraries)
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage caching
COPY requirements.txt .

# CRITICAL: Install dependencies directly with --no-cache-dir to save disk space
# We point to the CPU-only version of PyTorch explicitly here too just to be safe
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY ./app ./app

# Create a non-root user for security (Best Practice)
RUN useradd -m appuser
USER appuser

# Expose the port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]