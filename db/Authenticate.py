import pymongo
import bcrypt
import json
iNav = pymongo.MongoClient('mongodb://localhost:27017/')
iNavDB = iNav['iNavDB']

iNavCOL = iNavDB['Authentication']
print(" * INAVDB ",iNavDB)
print(" * INAVCOL ",iNavCOL)
print(" * Database connected !")

def add_new_user():
    global iNavDB
    mydict = { "_id": 1,"firstname": "Admin", "lastname": "Admin","email": "admin@atsp.com","username":"Admin","pssword": "password","status":1,"role":"Admin" }
    res = iNavCOL.insert_one(mydict)
    #res =iNavCOL.delete_many({})
    print(res)
    return res

def get_list():
    global iNavDB
    query = {}
    data = iNavCOL.find(query)
    return data