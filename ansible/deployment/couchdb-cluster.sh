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
