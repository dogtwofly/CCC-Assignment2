import re
import couchdb
import json


line = []
with open('/home/ubuntu/hostslist', 'r+') as f:
    lines = f.readlines()
    for i in range(len(lines)):
        line.append(lines[i])

for i in range(len(line)):
    if line[i].__contains__("db"):
        ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line[i+1])
        master = ip[0]
    if line[i].__contains__("slave"):
        ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line[i + 1])
        slave1 = ip[0]
        slave2 = ip[1]
masteraddress = "http://saaltfiish:huhuahua0124@"+str(master)+":5984/"
salveaddress1 = "http://saaltfiish:huhuahua0124@"+str(slave1)+":5984/"
salveaddress2 = "http://saaltfiish:huhuahua0124@"+str(slave2)+":5984/"

save={
  "_id": "829c9efbc7c367b0f927fa799100099a",
  "user_ctx": {
    "name": "saaltfiish",
    "roles": [
      "_admin",
      "_reader",
      "_writer"
    ]
  },
  "source": {
    "url": "http://localhost:5984/source",
    "headers": {
      "Authorization": "Basic c2FhbHRmaWlzaDpodWh1YWh1YTAxMjQ="
    }
  },
  "target": {
    "url": "http://{slave}:5984/source_copy",
    "headers": {
      "Authorization": "Basic c2FhbHRmaWlzaDpodWh1YWh1YTAxMjQ="
    }
  },
  "create_target": True,
  "continuous": True,
  "owner": "saaltfiish"
}

save['source']['url']=masteraddress
# print(save['source']['url'])
save['target']['url']=salveaddress1

couch = couchdb.Server(masteraddress)
try:
    db = couch.create('_replicator')  # create db table
except:
    db = couch['_replicator']

try:
    db.save(json.loads(save.encode('utf-8')))
except:
    pass

save["_id"] = "829c9efbc7c367b0f927fa799101123a"
save['target']['url']=salveaddress2
try:
    db = couch.create('_replicator')  # create db table
except:
    db = couch['_replicator']

try:
    db.save(json.loads(save.encode('utf-8')))
except:
    pass







