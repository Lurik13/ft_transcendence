FROM nginx:1.25.3
RUN rm -rf /var/www/html
RUN mkdir -p /etc/nginx/ssl
# COPY --from=build /app/frontend/dist /var/www/html
COPY nginx.conf /etc/nginx/nginx.conf
# COPY static/ /usr/share/nginx/html/static/
# COPY media/ /usr/share/nginx/html/media/
EXPOSE 8000
