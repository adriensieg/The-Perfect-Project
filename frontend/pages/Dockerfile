# Use the official Node.js image
FROM node:18-alpine

# Set the working directory
WORKDIR /usr/src/app

# Copy package.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the application code
COPY . .

# Build the Next.js app
RUN npm run build

# Expose port and run the app
EXPOSE 3000
CMD ["npm", "start"]
