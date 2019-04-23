import couchdb
import json

class tweetServer(couchdb.client.Server):
    def __init__(self, url, port, user, pwd):
        self.url = url
        self.port = port
        self.user = user
        self.pwd = pwd
        self.server = None
    
    def connect(self):
        server_loc = "http://{}:{}@{}:{}/".format(
            self.user, 
            self.pwd, 
            self.url, 
            self.port
            )
        self.server = couchdb.Server(server_loc)
        return self.server

    def getDB(self, label):
        db = tweetDB(self.server, label)
        return db

class tweetDB(couchdb.client.Database):
    def __init__(self, server, label):
        self.server = server
        self.label = label
        self.db = self.connect()
        
    def connect(self):
        self.db = self.server[self.label]
        return self.db

    def info(self):
        return self.db.info()

    def view(self, name):
        return self.db.view(name)

    def read(self, id):
        try:
            ret = self.db[id]
            return ret
        except couchdb.http.ResourceNotFound as e1:
            return None

    def create(self, doc):
        exist = self.read(doc['_id'])
        if(exist is None):
            id, rev = self.db.save(doc)
            print("doc: {}\ncreated\n".format(doc))
            return id, rev
        else:
            print("id already exists for doc\n{}\n{}\n".format(doc, exist))
            return None, None

    def delete(self, id):
        exist = self.read(id)
        if(exist is None):
            print("no existing doc with id: {}\n".format(id))
            return False
        else:
            self.db.delete(exist)
            print("doc with id: {} deleted\n".format(id))
            return True

    def update(self, doc):
        id = doc['_id']
        exist = self.read(id)
        if(exist is None):
            print("no existing doc with id: {}\n".format(id))
            return None, None
        else:
            doc['_rev'] = exist['_rev']
            ret = self.db.update([doc])
            print("doc: {}\nupdated with new doc:\n{}\n".format(exist, doc))
            return ret

    def compact(self):
        return self.db.compact()


if __name__ == "__main__":

    local_server = tweetServer("localhost", "6992", "saaltfiish", "huhuahua0124")
    local_server.connect()

    test1 = local_server.getDB("test1")

    doc1 = {'_id' : '7', 'name' : '罗云熙', 'update' : 1}
    test1.create(doc1)

    test1.delete("7")

    doc3 = {'_id': '1', 'name': '曾舜晞', 'update': '2'}
    doc4 = {'_id': '2', 'name': '陈钰琪', 'update': '2'}
    print(test1.update(doc3))
    print(test1.update(doc4))

    v1 = test1.view('test01/del')
    print(v1.rows)

    # print(test1.info())
    # print(test1.compact())
    # print(test1.info())