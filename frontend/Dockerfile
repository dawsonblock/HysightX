# frontend/Dockerfile
# Multi-stage build for the HysightX React/Vite frontend.
# Build context: repo root.

# ── Stage 1: build ────────────────────────────────────────────────────────────
FROM node:24-slim AS builder

WORKDIR /app/frontend

# Install Yarn 1.22.22 explicitly (matches package.json engines)
RUN npm install -g yarn@1.22.22 --quiet

# Copy manifests first for layer-cache efficiency
COPY frontend/package.json frontend/yarn.lock ./

# Install deps — skip preinstall script (verify-runtime.js) in CI/Docker
RUN yarn install --frozen-lockfile --ignore-scripts

# Copy full frontend source
COPY frontend/ ./

# Build args that become VITE_ env vars baked into the bundle
ARG VITE_BACKEND_URL=""
ENV VITE_BACKEND_URL=$VITE_BACKEND_URL

RUN yarn build

# ── Stage 2: serve ────────────────────────────────────────────────────────────
FROM nginx:1.27-alpine

# Remove default nginx config; inject ours
RUN rm /etc/nginx/conf.d/default.conf
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from builder
COPY --from=builder /app/frontend/build /usr/share/nginx/html

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
