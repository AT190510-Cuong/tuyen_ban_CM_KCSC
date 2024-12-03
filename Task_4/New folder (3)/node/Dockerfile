# Latest Node.js version at the time of writing
FROM node:22.6.0-alpine3.20

# Update and install any necessary dependencies
RUN apk update && rm -rf /var/cache/apk/*

# Set the working directory and create a non-root user
WORKDIR /home/app
RUN addgroup -S app && adduser -S app -G app

# Copy package.json and package-lock.json and install dependencies
COPY package*.json ./
RUN npm install && rm -rf /root/.npm  # Clean up npm cache for smaller image size

# Copy the rest of the application files and set ownership
COPY index.js .

# Change ownership of application files to root and make them read-only
RUN chown -R root:root /home/app && \
    chmod -R 555 /home/app

# Switch to the non-root user to avoid running as root
USER app

# Set environment variable for production
ENV NODE_ENV=production

# Expose the port the application listens on
EXPOSE 3000

# Start the Node.js application directly
CMD ["node", "/home/app/index.js"]
