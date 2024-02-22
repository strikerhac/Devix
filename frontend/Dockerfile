FROM node:16.16.0
RUN mkdir /frontend-app
WORKDIR /frontend-app
COPY package.json /frontend-app/package.json
COPY . /frontend-app/
RUN npm install
CMD ["npm", "start"]