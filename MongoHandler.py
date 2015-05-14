from pymongo import MongoClient
import csv, json, datetime, ast
from bson.json_util import dumps

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
            except (Exception), ex:
                print "Failed to import from csv \'%s\': %s" % (csv_filename, ex.message)

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
            except (Exception), ex:
                print "Failed to switch to collection \'%s\': %s" % (collection_name, ex.message)

        query = raw_input('Input Mongodb query (what you insert within collection.find()): ')
        query_dict = ast.literal_eval(query)
        cursor = collection.find(query_dict)
        print "Found %s rows in total" % cursor.count()
        
        try:
            f_json = open(json_filename, 'wb')
            f_json.write(dumps(cursor))
            f_json.close()
        except (Exception), ex:
            print "Saving json file failed: %s" % ex.message
        
        try:
            f_json = open(json_filename, 'r')
            data_json = json.load(f_json)
            f_json.close()
            f_csv = open(csv_filename, 'wb+')
            writer_csv = csv.writer(f_csv)
            writer_csv.writerow(data_json[0].keys())
            for row in data_json:
                try:
                    writer_csv.writerow(row.values())
                except (Exception), ex:
                    pass
        except (Exception), ex:
            print "Saving csv file failed: %s" % ex.message


    def timestamp_convert(self, timestamp=None):

        # Convert timestamp into year, month, and day
        if timestamp is None:
            return None
        else:
            timestamp_int = int(timestamp)
            time_result = {}
            time_result['year'] = datetime.datetime.fromtimestamp(timestamp_int).strftime('%Y')
            time_result['month'] = datetime.datetime.fromtimestamp(timestamp_int).strftime('%m')
            time_result['day'] = datetime.datetime.fromtimestamp(timestamp_int).strftime('%d')
            return time_result

    def l_profile_parser(self, linkedin_profile=None):
        if linkedin_profile is None:
            return None
        else:
            pass


    def c_profile_parser(self, crunchbase_profile):
        if crunchbase_profile = None:
            return None
        else:
            crunchbase_profile_relationship = crunchbase_profile['relationships']
            crunchbase_profile_headquarter = crunchbase_profile_relationship['headquarters']['items'][0]


    def cleanup(self):

        # Clean up data from database and insert into csv
        db_name = raw_input('Input name of db: ')
        collection_name = raw_input('Input name of collection: ')
        json_filename = raw_input('Input name of json file: ')
        csv_filename = raw_input('Input name of csv file: ')

        if db_name is not None and collection_name is not None and json_filename is not None:
            db = self.mongo_client[db_name]
            try:
                collection = db[collection_name]
            except (Exception), ex:
                print "Failed to switch to collection \'%s\': %s" % (collection_name, ex.message)

        cursor = collection.find().limit(1)
        print "Found %s rows in total" % cursor.count()
        
        try:
            f_json = open(json_filename, 'wb')
            f_json.write(dumps(cursor))
            f_json.close()
        except (Exception), ex:
            print "Saving json file failed: %s" % ex.message

        try:
            f_json = open(json_filename, 'r')
            data_raw_json = json.load(f_json)
            f_json.close()
            data_selected_json = []
            for data_raw in data_raw_json:
                data_temp = {}
                for field_name in ['name', 'location_city', 'location_country_code', 
                                   'location_region', 'primary_role', 'short_description']:
                    data_temp[field_name] = data_raw[field_name]
                data_temp.update(self.c_profile_parser(data_raw['crunchbase_profile']))
                data_temp.update(self.l_profile_parser(data_raw['linkedin_profile']))

            f_csv = open(csv_filename, 'wb+')
            writer_csv = csv.writer(f_csv)
            writer_csv.writerow(data_json[0].keys())
            for row in data_json:
                try:
                    writer_csv.writerow(row.values())
                except:
                    pass
        except (Exception), ex:
            print "Saving csv file failed: %s" % ex.message
        

        return None


if __name__ == "__main__":
    mh = MongoHandler()
    mh_mode = raw_input('Use Mongo Handler for csv data importing or query outputing? (i/o/c) ')
    if mh_mode == 'i':
        mh.insert_csv()
    elif mh_mode == 'o':
        mh.query_output_json_csv()
    elif mh_mode == 'c':
        mh.cleanup()
    else:
        print "Invalid mode selection"
