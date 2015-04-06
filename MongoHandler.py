from pymongo import MongoClient
import csv



class MongoHandler(object):

    def __init__(self):
        
        self.mongo_client = MongoClient()

    def insert_csv(self, db_name=None, collection_name=None, csv_filename=None):

        # Import data from csv file to MongoDB
        db_name = raw_input('Input name of db: ')
        collection_name = raw_input('Input name of collection: ')
        csv_filename = raw_input('Input name of csv file: ')
        
        if db_name is not None and collection_name is not None and csv_filename is not None:
            db = mongo_client[db_name]
            try:
                with open(csv_filename) as f:
                    records = csv.DictReader(f)
                    db[collection_name].insert(records)
            except:
                "Failed to import from csv"

        return None


if __name__ == "__main__":
    mh = MongoHandler()
    mh.insert_csv()