FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and sample files
COPY src/ ./src/
COPY samples/ ./samples/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the API
CMD ["uvicorn", "src.validator.api:app", "--host", "0.0.0.0", "--port", "8000"]