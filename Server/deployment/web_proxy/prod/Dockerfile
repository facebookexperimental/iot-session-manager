FROM nginx:alpine
WORKDIR /app/
COPY ./nginx-prod.conf /etc/nginx/nginx.conf

EXPOSE 80, 443

COPY ../../certs/prod_ssl ./ssl-certs

CMD ["nginx", "-g", "daemon off;"]
