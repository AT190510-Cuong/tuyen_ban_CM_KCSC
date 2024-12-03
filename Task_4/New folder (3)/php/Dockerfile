# Start with the official PHP Apache image
FROM php:8.0-apache

# Update and install necessary dependencies
RUN apt update && apt install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user and group
RUN useradd -ms /bin/bash ctfuser

# Copy the web application files
COPY src /var/www/html/
COPY init.sh /

# Set the ownership of the web files to root and make them read-only
RUN chown -R root:root /var/www/html && \
    chmod -R 555 /var/www/html && \
    chmod +x /init.sh

# Switch to the non-root user to prevent root access
USER ctfuser

# Expose the HTTP port
EXPOSE 80

# Run the initialization script (this should ideally start the server)
CMD ["/init.sh"]
