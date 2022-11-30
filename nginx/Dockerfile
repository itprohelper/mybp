FROM nginx:alpine
RUN mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak
COPY mbp.conf /etc/nginx/conf.d/
# tengo que copiar los static a /etc/nginx/html/static/? me sale el error