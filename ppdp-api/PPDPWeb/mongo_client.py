from pymongo import MongoClient

class MongoSevice:
    def connecttodb(self):
        try: 
            conn = MongoClient() 
        except:   
            print("Could not connect to MongoDB")  
        # database 
        db = conn.ppdp 
        # Created or Switched to collection names: my_gfg_collection 
        collection = db.sanitizeddata 
        return collection

    def connecttooriginaldb(self):
        try: 
            conn = MongoClient() 
        except:   
            print("Could not connect to MongoDB")  
        # database 
        db = conn.ppdp 
        # Created or Switched to collection names: my_gfg_collection 
        collection = db.unsanitizeddata 
        return collection

    def savetodb(self, collection, age, region, gender, job, religion, language, marital, sa, row):
        sanitized_record = { 
            "rowno": row,
            "age":age, 
            "region":region, 
            "gender":gender,
            "job": job,
            "religion": religion,
            "language": language,
            "marital": marital,
            "sa": sa
        } 
        collection.insert_one(sanitized_record) 

    def deleterecords(self, collection):
        collection.delete_many({})

    def countrows(self, collection, property):
        pipeline = [
            {"$group": {"_id": "$"+property, "count": {"$sum": 1}}}
        ]
        cursor = collection.aggregate(pipeline)
        return list(cursor)

    def find(self, collection):
        return pd.DataFrame(list(collection.find({}, {'_id':0})))



