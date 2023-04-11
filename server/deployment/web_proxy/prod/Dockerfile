FROM nginx:alpine
WORKDIR /app/
COPY ./nginx-prod.conf /etc/nginx/nginx.conf
CMD ["nginx", "-g", "daemon off;"]
