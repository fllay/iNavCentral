import pymongo
import bcrypt
iNav = pymongo.MongoClient('mongodb://localhost:27017/')
iNavDB = iNav['iNavDB']

iNavCOL = iNavDB['iNavDBlogs']
print(" * INAVDB ",iNavDB)
print(" * INAVCOL ",iNavCOL)
print(" * Database connected !")