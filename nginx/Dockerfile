# Nginx Dockerfile
FROM nginx:alpine

# Eliminar configuración por defecto
RUN rm /etc/nginx/conf.d/default.conf

# Exponer puerto
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
