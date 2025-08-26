FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy producer code
COPY producer.py /app/

# Install dependencies
RUN pip install kafka-python

# Command to run the producer
CMD ["python", "producer.py"]
