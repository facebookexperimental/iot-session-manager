FROM nginx:alpine
WORKDIR /app/
COPY ./nginx-dev.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
