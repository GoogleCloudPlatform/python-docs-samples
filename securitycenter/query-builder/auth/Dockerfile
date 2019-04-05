FROM nginx:1-alpine

# copy nginx configuration
COPY nginx/default.conf /etc/nginx/conf.d/

# expose port and define CMD
CMD ["nginx", "-g", "daemon off;"]