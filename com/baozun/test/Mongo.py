from pymongo import MongoClient
import json
myclient = MongoClient("mongodb://u_pem_sit:Zeu9JuajtDXUaNRv@ylf-sit-mongo-ross-public-db01.cloud.bz:27017/db_pem_sit")
myDb = myclient['db_pem_sit']
all_db_name = myDb.list_collection_names()
print(f"dbName {all_db_name}")
collection = myDb.get_collection('test')
data = collection.find().limit(10)
for d in data:
    print(f"data = {d}")
