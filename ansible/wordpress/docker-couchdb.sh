#!/bin/bash

docker pull couchdb
docker tag couchdb couchdb:local
docker images -a
docker run --name couchdb -e COUCHDB_USER=saaltfiish -e COUCHDB_PASSWORD=huhuahua0124 -p 5984:5984 -d couchdb:local
docker ps -a
sleep 10
curl -X PUT http://saaltfiish:huhuahua0124@127.0.0.1:5984/_users
curl -X PUT http://saaltfiish:huhuahua0124@127.0.0.1:5984/_replicator
curl -X PUT http://saaltfiish:huhuahua0124@127.0.0.1:5984/_global_changes

export nodes=(172.26.37.183 172.26.38.131 172.26.37.248)
export masternode=`echo ${nodes} | cut -f1 -d' '`
export othernodes=`echo ${nodes[@]} | sed s/${masternode}//`
export size=${#nodes[@]}
export username="saaltfiish"
export password="huhuahua0124"

for node in "${nodes[@]}"; do
    curl -XGET "http://${username}:${password}@${node}:5984/_all_dbs"
done

for node in "${nodes[@]}"; do
    curl -XPOST "http://${username}:${password}@${masternode}:5984/_cluster_setup" \
      --header "Content-Type: application/json" \
      --data "{\"action\": \"enable_cluster\", \
        \"bind_address\" : \"0.0.0.0\", \
        \"username\": \"${username}\", \"password\":\"${password}\", \"port\": \"5984\", \
        \"remote_node\": \"${node}\", \
        \"remote_current_user\":\"${username}\", \"remote_current_password\":\"${password}\"}"
done

for node in "${nodes[@]}"; do
    curl -XPOST "http://${username}:${password}@${masternode}:5984/_cluster_setup" \
      --header "Content-Type: application/json" \
      --data "{\"action\": \"add_node\", \"host\":\"${node}\", \
        \"port\": \"5984\", \"username\": \"${username}\", \"password\":\"${password}\"}"
done

#cat ~/password-docker | docker login --username saaltfiish --password-stdin
#docker start couchdb
#docker stop couchdb
#docker restart couchdb
