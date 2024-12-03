FROM node:14-slim

RUN apt-get update && apt-get install -y \
    tini \
    chromium \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

# Use tini to manage zombie processes and signal forwarding
ENTRYPOINT ["tini", "--"]

CMD ["npm", "start"]

EXPOSE 8000
