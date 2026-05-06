from pymongo import MongoClient

'''
    mongodb://ddc_adapter_jd_sit:D3J)hQ)ZWzB4Ruta5@ylf-sit-mongo-ross-public-db01.cloud.bz:27017,ylf-sit-mongo-ross-public-db02.cloud.bz:27017,ylf-sit-mongo-ross-public-db03.cloud.bz:27017/db_ddc_adapter_jd_sit?authSource=db_ddc_adapter_jd_sit&replicaSet=ross-sit-public-repl
'''

def test_mongodb():
    myclient = MongoClient("mongodb://ddc_adapter_jd_sit:D3J)hQ)ZWzB4Ruta5@ylf-sit-mongo-ross-public-db01.cloud.bz:27017?authSource=db_ddc_adapter_jd_sit")
    myDb = myclient['db_ddc_adapter_jd_sit']
    all_db_name = myDb.list_collection_names()
    print(f"dbName {all_db_name}")
    data = myDb.get_collection('vip_verify_info').find().limit(10)
    for d in data:
        print(d)

if __name__ == '__main__':
    test_mongodb()

