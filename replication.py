import re
import couchdb

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

couch = couchdb.Server(masteraddress)
couch1 = couchdb.Server(salveaddress1)
couch2 = couchdb.Server(salveaddress2)
db = couch['brandnew']
try:
    couch1.create('brandnew_copy1')
except:
    db1 = couch1['brandnew_copy1']
try:
    couch2.create('brandnew_copy2')
except:
    db2 = couch2['brandnew_copy2']
database = masteraddress+"brandnew"
subdatabase1 = salveaddress1+ "brandnew_copy1"
subdatabase2 = salveaddress2+ "brandnew_copy2"
couch.replicate(database, subdatabase1, coutinous=True)
couch.replicate(database, subdatabase2, coutinous=True)







