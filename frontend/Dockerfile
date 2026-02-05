FROM node:20-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
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
