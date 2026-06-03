FROM node:22-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

ARG VITE_API_URL=/api
ENV VITE_API_URL=$VITE_API_URL
ENV DOCKER_BUILD=true

RUN npm run build

# ---

FROM node:22-alpine

WORKDIR /app

COPY --from=builder /app/build ./build

EXPOSE 3000

ENV NODE_ENV=production

CMD ["node", "build"]
