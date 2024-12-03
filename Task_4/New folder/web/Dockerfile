FROM node:18-slim

WORKDIR /app

# Install packages
RUN apt-get update && \
    apt-get install -y postgresql-client curl && \
    rm -rf /var/lib/apt/lists/*

# Install node modules
COPY package*.json ./
RUN npm install --omit=dev

# Copy application files and set permissions
COPY . .

# Randomize the flag name, move it to root, and set it as read-only
RUN flag_name=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 16) && \
    mv /app/app/flag.txt /flag_$flag_name.txt && \
    chmod 444 /flag_$flag_name.txt && \
    chown root:root /flag_$flag_name.txt

# Set all files in /app to be read-only for www-data
RUN chown -R root:root /app && chmod -R 755 /app

# Set specific permissions for key files if needed
RUN chown root:www-data /app/private_key.pem && chmod 640 /app/private_key.pem

# Ensure the entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Switch to www-data for running the application
USER www-data

# Expose the port the application will run on
EXPOSE 80

# Start the application using the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
