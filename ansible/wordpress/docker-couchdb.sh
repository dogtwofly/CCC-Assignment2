#!/bin/bash

#apt-get install docker-ce docker-ce-cli containerd.io
#cat ~/password-docker | docker login --username saaltfiish --password-stdin
docker pull couchdb
docker tag couchdb couchdb:local
docker images -a
#docker push saaltfiish/common:couchdb
#docker create --name couchdb -p 5984:5984 couchdb:local
#docker start couchdb
#docker stop couchdb
#docker restart couchdb
#docker rm couchdb
#docker ps -a
docker run -e COUCHDB_USER=saaltfiish -e COUCHDB_PASSWORD=huhuahua0124 -p 5984:5984 -d couchdb:local
sleep 60
curl -X PUT http://saaltfiish:huhuahua0124@127.0.0.1:5984/_users
curl -X PUT http://saaltfiish:huhuahua0124@127.0.0.1:5984/_replicator
curl -X PUT http://saaltfiish:huhuahua0124@127.0.0.1:5984/_global_changes

#sudo docker rm -f $(sudo docker ps -a -q)
#sudo docker rmi -f $(sudo docker images -a -q)
