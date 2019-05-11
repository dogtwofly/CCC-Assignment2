#!/bin/bash

docker pull couchdb
docker tag couchdb couchdb:local
docker images -a
docker run --name couchdb -e COUCHDB_USER=saaltfiish -e COUCHDB_PASSWORD=huhuahua0124 -p 5984:5984 -d couchdb:local
docker ps -a
sleep 150
curl -X PUT http://saaltfiish:huhuahua0124@127.0.0.1:5984/_users
curl -X PUT http://saaltfiish:huhuahua0124@127.0.0.1:5984/_replicator
curl -X PUT http://saaltfiish:huhuahua0124@127.0.0.1:5984/_global_changes

