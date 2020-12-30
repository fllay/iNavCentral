import pymongo
import json
INAV = pymongo.MongoClient('mongodb://localhost:27017/')
INAV_DB = INAV['INAV_DB']
INAV_COL = INAV_DB['inav_logs']
print(" * INAV_DB ",INAV_DB)
print(" * INAV_COL ",INAV_COL)
print(" * Database connected !")
  
  
def add_new_one(col_name,data_dict):
    global INAV_DB
    new_col = INAV_DB[col_name]# Add new or append database collection  
    res = new_col.insert_one(data_dict)#Insert data into collection
    print(res)
    
def add_col(data_in):
    global INAV_DB
    colection = json.loads(data_in)
    colection = colection.colection
    col = INAV_DB[colection]
    res = col.insert_one(data_in)
    print(res)
    return res
    
def find_by_key(data_in):
    global INAV_DB
    colection = json.loads(data_in)
    colection = colection.colection
    find_col = INAV_DB[colection]
    res  = find_col.find_one()
    print(res)
    return res 

       