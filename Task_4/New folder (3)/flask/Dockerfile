FROM python:3.10-slim

# Create a non-root user and group
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip  # Clean up pip cache to reduce image size

# Copy the application files
COPY . .

# Set ownership of application files to root and make them read-only
RUN chown -R root:root /app && \
    chmod -R 555 /app

# Switch to non-root user to avoid running as root
USER appuser

# Set environment variable for production
ENV FLASK_ENV=production

# Expose the port the Flask app listens on
EXPOSE 5000

# Start the Flask app
CMD ["python", "app.py"]
