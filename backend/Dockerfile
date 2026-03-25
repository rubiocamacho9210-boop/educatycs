FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright with all system dependencies (replaces manual apt-get list)
RUN playwright install --with-deps chromium

# Copy application code
COPY . .

# Create .env file from example if not exists
RUN if [ ! -f .env ]; then cp .env.example .env; fi

# Expose port
EXPOSE 8000

# Run the application. Railway provides PORT dynamically.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
