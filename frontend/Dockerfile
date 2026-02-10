FROM node:20-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

FROM node:20-alpine

RUN addgroup -S appuser && adduser -S appuser -G appuser
RUN npm install -g serve

WORKDIR /app
COPY --from=build /app/dist ./dist
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5173
CMD ["serve", "-s", "dist", "-l", "5173"]
