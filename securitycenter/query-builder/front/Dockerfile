# ---- Base Node ----
FROM node:8.11.2-alpine AS build
# set working directory
WORKDIR /scc-query-builder
# copy project file
COPY package*json ./

RUN npm set progress=false && npm config set depth 0
RUN npm install

COPY . .
RUN  npm run build_prod

# ---- Release ----
FROM nginx:1-alpine

# copy nginx configuration
COPY nginx/default.conf /etc/nginx/conf.d/

WORKDIR /app

# copy app sources
COPY --from=build /scc-query-builder/dist/scc-query-builder/ /app/

# expose port and define CMD
CMD ["nginx", "-g", "daemon off;"]