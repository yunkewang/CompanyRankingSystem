from pymongo import MongoClient
import csv
import json
from bson.json_util import dumps
import ast

class MongoHandler(object):

    def __init__(self):
        
        self.mongo_client = MongoClient()

    def insert_csv(self, db_name=None, collection_name=None, csv_filename=None):

        # Import data from csv file to MongoDB
        db_name = raw_input('Input name of db: ')
        collection_name = raw_input('Input name of collection: ')
        csv_filename = raw_input('Input name of csv file: ')
        
        if db_name is not None and collection_name is not None and csv_filename is not None:
            db = self.mongo_client[db_name]
            try:
                with open(csv_filename) as f:
                    records = csv.DictReader(f)
                    db[collection_name].insert(records)
            except:
                print "Failed to import from csv %s" % csv_filename

        return None

    def query_output_json_csv(self, db_name=None, collection_name=None, json_filename=None):

        # Import data from csv file to MongoDB
        db_name = raw_input('Input name of db: ')
        collection_name = raw_input('Input name of collection: ')
        json_filename = raw_input('Input name of json file: ')
        csv_filename = raw_input('Input name of csv file: ')

        if db_name is not None and collection_name is not None and json_filename is not None:
            db = self.mongo_client[db_name]
            try:
                collection = db[collection_name]                
            except:
                print "Failed to switch to collection %s" % collection_name

        query = raw_input('Input Mongodb query (what you insert within collection.find()): ')
        query_dict = ast.literal_eval(query)
        cursor = collection.find(query_dict)
        
        try:
            f_json = open(json_filename, 'wb')
            f_json.write(dumps(cursor))
            f_json.close()
        except:
            print "Saving json file failed"
        
        try:
            f_json = open(json_filename, 'r')
            data_json = json.load(f_json)
            f_json.close()
            f_csv = open(csv_filename, 'wb+')
            writer_csv = csv.writer(f_csv)
            writer_csv.writerow(data_json[0].keys())
            for row in data_json:
                writer_csv.writerow(row.values())
        except:
            print "Saving csv file failed"


if __name__ == "__main__":
    mh = MongoHandler()
    mh_mode = raw_input('Use Mongo Handler for csv data importing or query outputing? (i/o) ')
    if mh_mode == 'i':
        mh.insert_csv()
    elif mh_mode == 'o':
        mh.query_output_json_csv()
    else:
        print "Invalid mode selection"
