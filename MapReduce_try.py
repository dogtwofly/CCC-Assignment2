import couchdb
# address1 = "http://saaltfiish:huhuahua0124@172.26.37.183:5984/"
server = couchdb.Server('http://saaltfiish:huhuahua0124@172.26.38.155:5984/')
db=server['brandnew']
try:
    db2=server.create('result')
except:
    db2=server['result']

Melbourne={
    "number":{
        "map":"function(doc){if(doc.place.full_name=='Melbourne, Victoria')emit(doc._id,1)}",
         "reduce":"function (key, values) {   return sum(values); }"},
    "profanity":{
        "map": "function(doc){if(doc.place.full_name=='Melbourne, Victoria'&& doc.profanity==true)emit(doc._id,1)}",
        "reduce": "function (key, values) {   return sum(values); }"},
    "crime":{
        "map": "function(doc){if(doc.place.full_name=='Melbourne, Victoria'&& doc.crime==true)emit(doc._id,1)}",
        "reduce": "function (key, values) {   return sum(values); }"},
    "wrath": {
        "map": "function(doc){if(doc.place.full_name=='Melbourne, Victoria'&& doc.wrath==true)emit(doc._id,1)}",
        "reduce": "function (key, values) {   return sum(values); }"},
    "lust":{
        "map":"function(doc){if(doc.place.full_name=='Melbourne, Victoria'&& doc.lust==true)emit(doc._id,1)}",
         "reduce":"function (key, values) {   return sum(values); }"},
}
Sydney={
    "number":{
        "map":"function(doc){if(doc.place.full_name=='Sydney, New South Wales')emit(doc._id,1)}",
         "reduce":"function (key, values) {   return sum(values); }"},
    "profanity":{
        "map": "function(doc){if(doc.place.full_name=='Sydney, New South Wales'&& doc.profanity==true)emit(doc._id,1)}",
        "reduce": "function (key, values) {   return sum(values); }"},
    "crime":{
        "map": "function(doc){if(doc.place.full_name=='Sydney, New South Wales'&& doc.crime==true)emit(doc._id,1)}",
        "reduce": "function (key, values) {   return sum(values); }"},
    "wrath": {
        "map": "function(doc){if(doc.place.full_name=='Sydney, New South Wales'&& doc.wrath==true)emit(doc._id,1)}",
        "reduce": "function (key, values) {   return sum(values); }"},
    "lust":{
        "map":"function(doc){if(doc.place.full_name=='Sydney, New South Wales'&& doc.lust==true)emit(doc._id,1)}",
         "reduce":"function (key, values) {   return sum(values); }"},
}
Perth={
    "number":{
        "map":"function(doc){if(doc.place.full_name=='Perth, Western Australia')emit(doc._id,1)}",
         "reduce":"function (key, values) {   return sum(values); }"},
    "profanity":{
        "map": "function(doc){if(doc.place.full_name=='Perth, Western Australia'&& doc.profanity==true)emit(doc._id,1)}",
        "reduce": "function (key, values) {   return sum(values); }"},
    "crime":{
        "map": "function(doc){if(doc.place.full_name=='Perth, Western Australia'&& doc.crime==true)emit(doc._id,1)}",
        "reduce": "function (key, values) {   return sum(values); }"},
    "wrath": {
        "map": "function(doc){if(doc.place.full_name=='Perth, Western Australia'&& doc.wrath==true)emit(doc._id,1)}",
        "reduce": "function (key, values) {   return sum(values); }"},
    "lust":{
        "map":"function(doc){if(doc.place.full_name=='Perth, Western Australia'&& doc.lust==true)emit(doc._id,1)}",
         "reduce":"function (key, values) {   return sum(values); }"},
}

Brisbane={
    "number":{
        "map":"function(doc){if(doc.place.full_name=='Brisbane, Queensland'||doc.place.full_name=='Brisbane City, Brisbane')emit(doc._id,1)}",
         "reduce":"function (key, values) {   return sum(values); }"},
    "profanity":{
        "map": "function(doc){if(doc.place.full_name=='Brisbane, Queensland'&& doc.profanity==true)emit(doc._id,1)}",
        "reduce": "function (key, values) {   return sum(values); }"},
    "crime":{
        "map": "function(doc){if(doc.place.full_name=='Brisbane, Queensland'&& doc.crime==true)emit(doc._id,1)}",
        "reduce": "function (key, values) {   return sum(values); }"},
    "wrath": {
        "map": "function(doc){if(doc.place.full_name=='Brisbane, Queensland'&& doc.wrath==true)emit(doc._id,1)}",
        "reduce": "function (key, values) {   return sum(values); }"},
    "lust":{
        "map":"function(doc){if(doc.place.full_name=='Brisbane, Queensland'&& doc.lust==true)emit(doc._id,1)}",
         "reduce":"function (key, values) {   return sum(values); }"},
}

Adelaide={
    "number":{
        "map":"function(doc){if(doc.place.full_name=='Adelaide, South Australia')emit(doc._id,1)}",
         "reduce":"function (key, values) {   return sum(values); }"},
    "profanity":{
        "map": "function(doc){if(doc.place.full_name=='Adelaide, South Australia'&& doc.profanity==true)emit(doc._id,1)}",
        "reduce": "function (key, values) {   return sum(values); }"},
    "crime":{
        "map": "function(doc){if(doc.place.full_name=='Adelaide, South Australia'&& doc.crime==true)emit(doc._id,1)}",
        "reduce": "function (key, values) {   return sum(values); }"},
    "wrath": {
        "map": "function(doc){if(doc.place.full_name=='Adelaide, South Australia'&& doc.wrath==true)emit(doc._id,1)}",
        "reduce": "function (key, values) {   return sum(values); }"},
    "lust":{
        "map":"function(doc){if(doc.place.full_name=='Adelaide, South Australia'&& doc.lust==true)emit(doc._id,1)}",
         "reduce":"function (key, values) {   return sum(values); }"},
}

Canberra={
    "number":{
        "map":"function(doc){if(doc.place.full_name=='Canberra, Australian Capital Territory')emit(doc._id,1)}",
         "reduce":"function (key, values) {   return sum(values); }"},
    "profanity":{
        "map": "function(doc){if(doc.place.full_name=='Canberra, Australian Capital Territory'&& doc.profanity==true)emit(doc._id,1)}",
        "reduce": "function (key, values) {   return sum(values); }"},
    "crime":{
        "map": "function(doc){if(doc.place.full_name=='Canberra, Australian Capital Territory'&& doc.crime==true)emit(doc._id,1)}",
        "reduce": "function (key, values) {   return sum(values); }"},
    "wrath": {
        "map": "function(doc){if(doc.place.full_name=='Canberra, Australian Capital Territory'&& doc.wrath==true)emit(doc._id,1)}",
        "reduce": "function (key, values) {   return sum(values); }"},
    "lust":{
        "map":"function(doc){if(doc.place.full_name=='Canberra, Australian Capital Territory'&& doc.lust==true)emit(doc._id,1)}",
         "reduce":"function (key, values) {   return sum(values); }"},
}

def creat_design_doc(key, views):
    try:
        db[key] = dict(language='javascript', views=views)
    except:
        del db[key]
        db[key] = dict(language='javascript', views=views)


def get_result_first(views, key, value):
    for row in db.view(views):
        print(row)
        p={value:row.value}
        try:
            db2[key]=dict(p)

        except:
            del db2[key]
            db2[key] = dict(p)
def get_result_other(views, key, value):
    for row in db.view(views):
        print(row)
        data=db2[key]
        data[value]=row.value
        db2.save(data)


creat_design_doc('_design/Melbourne', Melbourne)
creat_design_doc('_design/Sydney', Sydney)
creat_design_doc('_design/Perth', Perth)
creat_design_doc('_design/Brisbane', Brisbane)
creat_design_doc('_design/Adelaide', Adelaide)
creat_design_doc('_design/Canberra', Canberra)
location ={'Melbourne':Melbourne, 'Sydney':Sydney, 'Perth':Perth,'Brisbane':Brisbane, 'Adelaide':Adelaide, 'Canberra':Canberra}
query={}
detail=['number','profanity','crime','wrath','lust']
name=['Count','Profanity','Crime','Wrath','Lust']
for key, value in location.items():
    for i in range(len(detail)):
        query[key+'/'+detail[i]]=str(name[i])

count =0
for x, y in query.items():
    if count ==0:
        get_result_first(x,"Melbourne",y)
        count += 1
    elif count>0 and count<5:
        get_result_other(x,"Melbourne",y)
        count += 1
    elif count == 5:
        get_result_first(x, "Sydney", y)
        count += 1
    elif count>5 and count<10:
        get_result_other(x,"Sydney",y)
        count += 1
    elif count == 10:
        get_result_first(x, "Perth", y)
        count += 1
    elif count>10 and count<15:
        get_result_other(x,"Perth",y)
        count += 1
    elif count == 15:
        get_result_first(x, "Brisbane", y)
        count += 1
    elif count>15 and count<20:
        get_result_other(x,"Brisbane",y)
        count += 1
    elif count == 20:
        get_result_first(x, "Adelaide", y)
        count += 1
    elif count>20 and count<25:
        get_result_other(x,"Adelaide",y)
        count += 1
    elif count == 25:
        get_result_first(x, "Canberra", y)
        count += 1
    elif count>25 and count<30:
        get_result_other(x,"Canberra",y)
        count += 1



