FROM node:18.17.0

WORKDIR /usr/src/app/

COPY package*.json ./

RUN yarn install

EXPOSE 3000

CMD ["yarn", "start"]