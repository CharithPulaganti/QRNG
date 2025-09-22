FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install || true
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]
