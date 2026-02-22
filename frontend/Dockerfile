FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

# Source is mounted via docker-compose volume at runtime
CMD ["npx", "vite", "--host", "0.0.0.0"]
