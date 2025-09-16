FROM node:20 as build

WORKDIR /client
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /client/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf