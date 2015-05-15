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
        print "Found %s rows in total" % cursor.count()
        
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
                try:
                    writer_csv.writerow(row.values())
                except:
                    pass
        except:
            print "Saving csv file failed"


    def timestamp_convert(self, timestamp=None):

        # Convert timestamp into year, month, and day
        if timestamp is None:
            return {'year': 'null', 'month': 'null', 'day': 'null'}
        else:
            timestamp_int = timestamp
            time_result = {}
            time_result['year'] = datetime.datetime.fromtimestamp(timestamp_int).strftime('%Y')
            time_result['month'] = datetime.datetime.fromtimestamp(timestamp_int).strftime('%m')
            time_result['day'] = datetime.datetime.fromtimestamp(timestamp_int).strftime('%d')
            return time_result


    def timestring_parser(self, timestring=None):

        # Convert timestring into year, month, and day
        if timestring is None:
            return {'year': 'null', 'month': 'null', 'day': 'null'}
        else:
            time_dict = {}
            time = datetime.datetime.strptime(timestring, "%Y-%m-%d")
            time_dict['year'] = time.strftime('%Y')
            time_dict['month'] = time.strftime('%m')
            time_dict['day'] = time.strftime('%d')
            return time_dict


    def l_profile_parser(self, linkedin_profile=None):
        if linkedin_profile is None:
            return None
        else:
            pass


    def c_profile_parser(self, crunchbase_profile=None):
        
        null = None
        true = True
        false = False
        
        key_list = ['headquarter_longtitude', 'headquarter_latitude', 
                    'acquired_by_last', 'acquired_by_year', 'acquired_by_month', 'acquired_by_times', 
                    'competitors', 'competitors_amount', 
                    'offices1_city', 'offices1_state', 'offices2_city', 
                    'offices2_state', 'offices3_city', 'offices3_state', 'offices_amount', 
                    'recent_news1', 'recent_news2', 'recent_news3', 
                    'recent_news1_year', 'recent_news2_year', 'recent_news3_year',
                    'product1', 'product2', 'product3', 'products_amount',
                    'funding_last1', 'funding_last1_year', 
                    'funding_last2', 'funding_last2_year', 
                    'funding_last3', 'funding_last3_year', 
                    'funding_total', 'funding_total_rounds', 
                    'investors', 'founded_year', 'founded_month', 'founded_day',
                    'inverstments_number', 'is_closed', 'catogory_keyword1',
                    'catogory_keyword2', 'catogory_keyword3', 'catogory_keyword4',
                    'catogory_keyword5'
                    ]
        result_dict = dict.fromkeys(key_list)
        
        if crunchbase_profile is None:
            return result_dict
        else:
            crunchbase_profile_relationship = crunchbase_profile['data']['relationships']
            try:
                crunchbase_profile_headquarter = crunchbase_profile_relationship['headquarters']['items'][0]
                result_dict['headquarter_longtitude'] = crunchbase_profile_headquarter['longtitude']
                result_dict['headquarter_latitude'] = crunchbase_profile_headquarter['latitude']
            except (Exception), ex:
                pass
            try:
                crunchbase_profile_acquisition = crunchbase_profile_relationship['acquired_by']
                result_dict['acquired_by_last'] = crunchbase_profile_acquisition['items'][0]['name'].replace(',', '')
                acquired_time = crunchbase_profile_acquisition['items'][0]['announced_on']
                acquired_time_dict = self.timestring_parser(acquired_time)
                result_dict['acquired_by_year'] = acquired_time_dict['year']
                result_dict['acquired_by_month'] = acquired_time_dict['month']
                result_dict['acquired_by_times'] = crunchbase_profile_acquisition['paging']['total_items']
            except (Exception), ex:
                pass
            try:
                crunchbase_profile_offices = crunchbase_profile_relationship['offices']
                result_dict['offices_amount'] = crunchbase_profile_offices['paging']['total_items']
                for i in range(min(result_dict['offices_amount'], 3)):
                    result_dict['offices%s_city' % str(i + 1)] = crunchbase_profile_offices['items'][i]['city']
                    result_dict['offices%s_state' % str(i + 1)] = crunchbase_profile_offices['items'][i]['state']
            except (Exception), ex:
                pass
            try:
                crunchbase_profile_fundings = crunchbase_profile_relationship['funding_rounds']
                result_dict['funding_total_rounds'] = crunchbase_profile_fundings['paging']['total_items']
                for i in range(min(result_dict['offices_amount'], 3)):
                    result_dict['funding_last%s' % str(i + 1)] = crunchbase_profile_fundings['items'][i]['name'].replace(',', '')
                    result_dict['funding_last%s_year' % str(i + 1)] = self.timestamp_convert(crunchbase_profile_fundings['items'][i]['created_at'])['year']
            except (Exception), ex:
                pass
            try:
                crunchbase_profile_news = crunchbase_profile_relationship['news']
                news_amount = crunchbase_profile_news['paging']['total_items']
                for i in range(min(news_amount, 3)):
                    result_dict['recent_news%s' % str(i + 1)] = crunchbase_profile_news['items'][i]['title'].replace(',', '')
                    result_dict['recent_news%s_year' % str(i + 1)] = self.timestamp_convert(crunchbase_profile_news['items'][i]['created_at'])['year']
            except (Exception), ex:
                pass
            try:
                crunchbase_profile_products = crunchbase_profile_relationship['products']
                result_dict['products_amount'] = crunchbase_profile_products['paging']['total_items']
                for i in range(min(result_dict['products_amount'], 3)):
                    result_dict['product%s' % str(i + 1)] = crunchbase_profile_products['items'][i]['name'].replace(',', '')
            except (Exception), ex:
                pass

            return result_dict



    def cleanup(self):

        # Clean up data from database and insert into csv
        db_name = raw_input('Input name of db: ')
        collection_name = raw_input('Input name of collection: ')
        json_filename = raw_input('Input name of json file: ')
        csv_filename = raw_input('Input name of csv file: ')

        null = None
        true = True
        false = False

        if db_name is not None and collection_name is not None and json_filename is not None:
            db = self.mongo_client[db_name]
            try:
                collection = db[collection_name]
            except:
                print "Failed to switch to collection %s" % collection_name

        cursor = collection.find()
        print "Found %s rows in total" % cursor.count()
        
        try:
            f_json = open(json_filename, 'wb')
            f_json.write(dumps(cursor))
            f_json.close()
        except:
            print "Saving json file failed"

        try:
            f_json = open(json_filename, 'r')
            data_raw_json = json.load(f_json)
            f_json.close()
            data_selected_json = []
            for data_raw in data_raw_json:
                data_temp = {}
                for field_name in ['name', 'location_city', 'location_country_code', 
                                   'location_region', 'primary_role', 'short_description']:
                    data_temp[field_name] = data_raw[field_name].replace(',', '')
                try:
                    data_temp.update(self.c_profile_parser(data_raw['crunchbase_profile']))
                except (Exception), ex:
                    continue
                # data_temp.update(self.l_profile_parser(data_raw['linkedin_profile']))
                data_selected_json.append(data_temp)

            f_csv = open(csv_filename, 'wb+')
            writer_csv = csv.writer(f_csv)
            writer_csv.writerow(data_selected_json[0].keys())
            for row in data_selected_json:
                try:
                    writer_csv.writerow(row.values())
                except:
                    pass
        except (Exception), ex:
            print "Saving csv file failed: %s" % ex.message
        

        return None


if __name__ == "__main__":
    # null = None
    # true = True
    # false = False
    mh = MongoHandler()
    # print mh.c_profile_parser(c_profile['crunchbase_profile'])
    mh_mode = raw_input('Use Mongo Handler for csv data importing or query outputing? (i/o/c) ')
    if mh_mode == 'i':
        mh.insert_csv()
    elif mh_mode == 'o':
        mh.query_output_json_csv()
    elif mh_mode == 'c':
        mh.cleanup()
    else:
        print "Invalid mode selection"
