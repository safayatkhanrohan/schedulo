# Stage 1: Build the Next.js app
FROM node:22-bullseye AS builder

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install --omit=dev

# Copy source code
COPY . .

# Build Next.js app
RUN npm run build

# Stage 2: Run the Next.js app (production)
FROM node:22-bullseye AS runner

WORKDIR /app

ENV NODE_ENV=production

# Copy built files + node_modules from builder
COPY --from=builder /app/next.config.ts ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# Expose Next.js port
EXPOSE 3000

# Start Next.js production server
CMD ["npm", "start"]
