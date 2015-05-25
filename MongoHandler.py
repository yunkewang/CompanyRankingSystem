from pymongo import MongoClient
import csv, json, datetime, ast, re
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

        null = None
        true = True
        false = False
        
        key_list_general = ['industry', 'num_linkedin_followers', 'employee_range_code', 'employee_range', 
                            'isPublic'
                           ]
        key_list_industry = [
                             'industry_Computer Software', 'industry_Printing', 'industry_Medical Device',
                             'industry_Computer Games', 'industry_Graphic Design', 'industry_Legal Services',
                             'industry_Internet', 'industry_Hospital & Health Care', 'industry_Leisure & Travel',
                             'industry_Information Technology & Services', 'industry_Food & Beverages',
                             'industry_Professional Training', 'industry_Online Publishing', 'industry_Real Estate',
                             'industry_Design', 'industry_Marketing & Advertising', 'industry_Restaurants',
                             'industry_Retail', 'industry_Entertainment', 'industry_Motion Pictures & Film',
                             'industry_Airlines/Aviation', 'industry_Market Research', 'industry_Information Services',
                             'industry_Sports', 'industry_Biotechnology', 'industry_Telecommunications',
                             'industry_Media Production', 'industry_Wireless', 'industry_Music',
                             'industry_Banking', 'industry_Logistics & Supply Chain', 'industry_Renewables & Environment',
                             'industry_Computer Hardware', 'industry_Management Consulting', 'industry_Consumer Goods',
                             'industry_Consumer Services', 'industry_E-learning', 'industry_Nonprofit Organization Management',
                             'industry_Publishing', 'industry_Medical Practice', 'industry_Financial Services',
                             'industry_Accounting', 'industry_Education Management', 'industry_Apparel & Fashion', 
                             'industry_Wholesale', 'industry_Staffing & Recruiting', 'industry_Luxury Goods & Jewelry',
                             'industry_Outsourcing/Offshoring', 'industry_Human Resources', 'industry_Law Enforcement',
                             'industry_Industrial Automation', 'industry_Automative', 'industry_Computer & Network Security',
                             'industry_Security & Investigations', 'industry_Higher Education', 'industry_Construction',
                             'industry_Insurance', 'industry_Government Relations'
                            ]

        result_dict = dict.fromkeys(key_list_general)
        
        if linkedin_profile is None:
            return result_dict
        else:
            
            try:
                industry_dict = dict.fromkeys(key_list_industry, 0)
                try:
                    linkedin_profile_industries = linkedin_profile['industries']['values']
                    for industry in linkedin_profile_industries:
                        if ("industry_%s" % industry['name'].encode('ascii', 'ignore').replace(',', '')) in industry_dict.keys():
                            industry_dict[("industry_%s" % industry['name'].encode('ascii', 'ignore').replace(',', ''))] = 1
                        else:
                            # print industry['name']
                            pass
                    # result_dict['industry'] = linkedin_profile_industries['name']
                except (Exception), ex:
                    pass
                result_dict.update(industry_dict)
            except (Exception), ex:
                # print ex.message
                pass
            
            try:
                result_dict['num_linkedin_followers'] = linkedin_profile['numFollowers']
            except (Exception), ex:
                # print ex.message
                pass
            
            try:
                linkedin_profile_employeerange = linkedin_profile['employeeCountRange']
                result_dict['employee_range_code'] = linkedin_profile_employeerange['code']
                result_dict['employee_range'] = linkedin_profile_employeerange['name']
            except (Exception), ex:
                # print ex.message
                pass
            
            try:
                linkedin_profile_type = linkedin_profile['companyType']
                if linkedin_profile_type['name'] == "Public":
                    result_dict['isPublic'] = True
                else:
                    result_dict['isPublic'] = False
            except (Exception), ex:
                # print ex.message
                pass

            return result_dict


    def c_profile_parser(self, crunchbase_profile=None):
        
        null = None
        true = True
        false = False
        
        key_list_general = ['headquarter_longitude', 'headquarter_latitude', 
                            'acquired_by_last', 'acquired_by_year', 'acquired_by_month', 'acquired_by_times', 
                            'competitor1', 'competitor2', 'competitor3', 'competitors_amount', 
                            'offices1_city', 'offices1_region', 'offices2_city', 
                            'offices2_region', 'offices3_city', 'offices3_region', 'offices_amount', 
                            'recent_news1', 'recent_news2', 'recent_news3', 
                            'recent_news1_year', 'recent_news2_year', 'recent_news3_year',
                            'product1', 'product2', 'product3', 'products_amount',
                            'funding_last1', 'funding_last1_year', 
                            'funding_last2', 'funding_last2_year', 
                            'funding_last3', 'funding_last3_year', 
                            'funding_total', 'funding_total_rounds', 'funding_total_amount',
                            'investors_amount', 'investor1', 'investor2', 'investor3',
                            'founded_year', 'founded_month', 'founded_day',
                            'is_closed'
                           ]
                    # 'category_keyword1', 'category_keyword2', 
                    # 'category_keyword3', 'category_keyword4', 'category_keyword5'
                    # ]

        key_list_category = ['category_Ad Targeting', 'category_Advertising', 'category_Advertising Platforms', 
                             'category_Agriculture', 'category_Analytics', 'category_Android', 
                             'category_App Marketing', 'category_Apps', 'category_Art', 'category_Artists Globally', 
                             'category_Audio', 'category_Automotive', 'category_Babies', 'category_B2B', 'category_Beauty',
                             'category_Big Data', 'category_Big Data Analytics', 'category_Biotechnology', 
                             'category_Blogging Platforms', 'category_Brand Marketing', 'category_Business Information Systems',
                             'category_Business Intelligence', 'category_Business Services', 'category_Career Planning',
                             'category_Career Management', 'category_Charity', 'category_Chat', 'category_Classifieds',
                             'category_Clean Technology', 'category_Cloud Computing', 'category_Cloud Management', 
                             'category_Cloud Data Services', 'category_Coffee', 'category_Celebrity', 'category_Curated Web',
                             'category_Collaboration', 'category_Computers', 'category_Construction', 'category_Consulting',
                             'category_Consumer Electronics', 'category_Consumers', 'category_Content', 'category_Content Discovery', 'category_Content Delivery', 
                             'category_Contests', 'category_Corporate Training', 'category_Corporate Wellness', 'category_Crowingfunding', 
                             'category_Coupons', 'category_CRM', 'category_Cureted Web', 'category_Creative', 'category_Cyber Security',
                             'category_Data Security', 'category_Delivery', 'category_Design', 'category_Data Centers', 'category_Data Mining',
                             'category_Data Visualization', 'category_Developer Tools', 'category_Development Platforms', 'category_Databases',
                             'category_Diagnostics', 'category_Digital Media', 'category_Domains', 'category_Data Privacy', 
                             'category_E-Commerce', 'category_E-Commerce Platforms', 'category_Electronics', 'category_Ediscovery', 'category_EdTech',
                             'category_Education', 'category_Employment', 'category_Enterprise Software',
                             'category_Enterprises', 'category_Entertainment', 'category_Entrepreneur',
                             'category_Environment Innovation', 'category_Environmental Innovation', 'category_Events', 'category_Fashion', 'category_Finance', 
                             'category_Finance Technology', 'category_Field Support Services', 'category_File Sharing', 
                             'category_Financing', 'category_Financial Services', 'category_FinTech', 'category_Games', 'category_Google Apps',
                             'category_Game', 'category_Gift Card', 'category_Gps', 'category_Graphics', 'category_Groceries',
                             'category_Hardware', 'category_Hardware + Software', 'category_Health Care', 'category_Health and Wellness', 
                             'category_Health Diagnostics', 'category_Home Automation', 'category_Hospitality',
                             'category_Human Resources', 'category_Information Services', 'category_Information Technology',
                             'category_Infrastructure', 'category_Internet', 'category_Internet of Things', 'category_Internet Marketing',
                             'category_iOS', 'category_iPad', 'category_iPhone', 'category_Jewelry',
                             'category_Language Learning', 'category_Law Enforcement', 'category_Linux',
                             'category_Local Business', 'category_Location Based Services',
                             'category_M2M', 'category_Manufacturing', 'category_Maps', 
                             'category_Market Research', 'category_Marketing Automation', 'category_Machine Learning', 
                             'category_Marketplaces', 'category_Media', 'category_Medical Devices',
                             'category_Messaging', 'category_MicroBlogging', 'category_Mobile', 'category_Mobile Commerce', 'category_Mobile Video',
                             'category_Mobile Payments', 'category_Monetization', 'category_Music',
                             'category_Networking', 'category_Network Security', 'category_New Product Deployment', 
                             'category_News', 'category_Nonprofits', 'category_Online Travel', 'category_Online Advertising', 'category_Online Shopping',
                             'category_Optimization', 'category_Outdoors', 'category_Online Rental', 'category_Payments', 'category_Online Scheduling',
                             'category_PC Gaming', 'category_Peer-to-Peer', 'category_Performance Marketing', 'category_PaaS', 
                             'category_Personal Data', 'category_Pets', 'category_Photography', 'category_Photo Sharing', 'category_Private Social Networking', 
                             'category_Portals', 'category_Predictive Analytics', 'category_Product Development Services',
                             'category_Productivity Software', 'category_Project Management', 'category_Property Management',
                             'category_Public Relations', 'category_Public Transportation', 'category_Publishing', 'category_Real Estate', 'category_Real Time',
                             'category_Recruiting', 'category_Restaurants', 'category_Retail', 
                             'category_Reviews and Recommendations', 'category_SaaS', 'category_Search',
                             'category_Search Marketing', 'category_Security', 'category_Services', 'category_Sales and Marketing',
                             'category_Shoes', 'category_Shopping', 'category_Small and Medium Business',
                             'category_Social + Mobile + Local', 'category_Social Business', 'category_Social Media', 'category_Social Commerce',
                             'category_Social Media Management', 'category_Social Media Marketing', 'category_Social Media Monitoring', 
                             'category_Social Network Media', 'category_Social Television', 'category_Software', 
                             'category_Sports', 'category_Startups', 'category_Storage', 'category_Surveys',
                             'category_Task Management', 'category_Tablets', 'category_Telecommunications', 'category_Television', 'category_Technology',
                             'category_Tech Field Support', 'category_Testing', 'category_Therapeutics', 'category_Tracking', 'category_Transportation',
                             'category_Travel', 'category_Twitter Application', 'category_Twitter Applications', 'category_Venture Capital', 'category_Video Conferencing', 'category_Video', 
                             'category_Video Streaming', 'category_Virtualization', 'category_VoIP', 'category_Visualization', 
                             'category_Water Purification', 'category_Web CMS', 'category_Web Development', 'category_Web Tools', 
                             'category_Web Hosting', 'category_Web Design', 'category_Wine And Spirits'
                            ]

        result_dict = dict.fromkeys(key_list_general)
        
        if crunchbase_profile is None:
            return result_dict
        else:
            crunchbase_profile_relationship = crunchbase_profile['data']['relationships']
            crunchbase_profile_properties = crunchbase_profile['data']['properties']
            
            try:
                crunchbase_profile_headquarter = crunchbase_profile_relationship['headquarters']['items'][0]
                result_dict['headquarter_longitude'] = crunchbase_profile_headquarter['longitude']
                result_dict['headquarter_latitude'] = crunchbase_profile_headquarter['latitude']
            except (Exception), ex:
                pass
            
            try:
                crunchbase_profile_acquisition = crunchbase_profile_relationship['acquired_by']
                result_dict['acquired_by_last'] = crunchbase_profile_acquisition['items'][0]['name'].encode('ascii', 'ignore').replace(',', '')
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
                    try:
                        result_dict['offices%s_city' % str(i + 1)] = crunchbase_profile_offices['items'][i]['city']
                        result_dict['offices%s_region' % str(i + 1)] = crunchbase_profile_offices['items'][i]['region']
                    except (Exception), ex:
                        print ex.message
                        continue
            except (Exception), ex:
                pass
            
            try:
                crunchbase_profile_fundings = crunchbase_profile_relationship['funding_rounds']
                result_dict['funding_total_rounds'] = crunchbase_profile_fundings['paging']['total_items']
                for i in range(min(result_dict['offices_amount'], 3)):
                    try:
                        result_dict['funding_last%s' % str(i + 1)] = crunchbase_profile_fundings['items'][i]['name'].encode('ascii', 'ignore').replace(',', '')
                        result_dict['funding_last%s_year' % str(i + 1)] = self.timestamp_convert(crunchbase_profile_fundings['items'][i]['created_at'])['year']
                    except (Exception), ex:
                        continue
            except (Exception), ex:
                pass
            
            try:
                crunchbase_profile_news = crunchbase_profile_relationship['news']
                news_amount = crunchbase_profile_news['paging']['total_items']
                for i in range(min(news_amount, 3)):
                    try:
                        result_dict['recent_news%s' % str(i + 1)] = crunchbase_profile_news['items'][i]['title'].encode('ascii', 'ignore').replace(',', '')
                        result_dict['recent_news%s_year' % str(i + 1)] = self.timestamp_convert(crunchbase_profile_news['items'][i]['created_at'])['year']
                    except (Exception), ex:
                        continue
            except (Exception), ex:
                pass
            
            try:
                crunchbase_profile_products = crunchbase_profile_relationship['products']
                result_dict['products_amount'] = crunchbase_profile_products['paging']['total_items']
                for i in range(min(result_dict['products_amount'], 3)):
                    try:
                        result_dict['product%s' % str(i + 1)] = crunchbase_profile_products['items'][i]['name'].encode('ascii', 'ignore').replace(',', '')
                    except:
                        continue
            except (Exception), ex:
                pass
            
            try:
                crunchbase_profile_competitors = crunchbase_profile_relationship['competitors']
                result_dict['competitors_amount'] = crunchbase_profile_competitors['paging']['total_items']
                for i in range(min(result_dict['competitors_amount'], 3)):
                    try:
                        result_dict['competitor%s' % str(i + 1)] = crunchbase_profile_competitors['items'][i]['name'].encode('ascii', 'ignore').replace(',', '')
                    except (Exception), ex:
                        continue
            except (Exception), ex:
                pass
            
            try:
                result_dict['funding_total_amount'] = crunchbase_profile_properties['total_funding_usd']
                result_dict['founded_year'] = crunchbase_profile_properties['founded_on_year']
                result_dict['founded_month'] = crunchbase_profile_properties['founded_on_month']
                result_dict['founded_day'] = crunchbase_profile_properties['founded_on_day']
                try:
                    investor_list = crunchbase_profile_properties.get('investors')
                    if investor is None:
                        pass
                    else:
                        result_dict['investors_amount'] = len(investor_list)
                        for i in range(min(result_dict['investors_amount'], 3)):
                            try:
                                result_dict['investor%s' % str(i + 1)] = investor_list[i]['name'].encode('ascii', 'ignore').replace(',', '')
                            except (Exception), ex:
                                continue
                except:
                    pass
                result_dict['is_closed'] = crunchbase_profile_properties['is_closed']
            except (Exception), ex:
                pass
            
            try:
                category_dict = dict.fromkeys(key_list_category, 0)
                try: 
                    crunchbase_profile_categories = crunchbase_profile_relationship['categories']
                    categories_amount = crunchbase_profile_categories['paging']['total_items']
                    for item in crunchbase_profile_categories['items']:
                        try:
                            if ("category_%s" % item['name'].encode('ascii', 'ignore').replace(',', '')) in category_dict.keys():
                                category_dict[("category_%s" % item['name'].encode('ascii', 'ignore').replace(',', ''))] = 1
                            else:
                                # print "category_%s" % item['name'].encode('ascii', 'ignore').replace(',', '')
                                pass
                        except (Exception), ex:
                            print ex.message
                            continue
                except (Exception), ex:
                    pass
                result_dict.update(category_dict)
                # for i in range(min(categories_amount, 5)):
                #     try:
                #         result_dict['category_keyword%s' % str(i + 1)] = crunchbase_profile_categories['items'][i]['name'].encode('ascii', 'ignore').replace(',', '')
                #     except (Exception), ex:
                #         print ex.message
                #         continue
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
                    data_temp[field_name] = re.sub(r'\\', r',', data_raw[field_name].encode('ascii', 'ignore').replace(',', ''))
                try:
                    data_temp.update(self.c_profile_parser(data_raw['crunchbase_profile']))
                except (Exception), ex:
                    print "Failed to parse Crunchbase profile: %s" % ex.message
                    continue
                try:
                    data_temp.update(self.l_profile_parser(data_raw['linkedin_profile']))
                except (Exception), ex:
                    print "Failed to parse LinkedIn profile: %s" % ex.message
                    continue
                data_selected_json.append(data_temp)

            f_csv = open(csv_filename, 'wb+')
            writer_csv = csv.writer(f_csv)
            writer_csv.writerow(data_selected_json[0].keys())
            for row in data_selected_json:
                try:
                    writer_csv.writerow(row.values())
                except (Exception), ex:
                    print "Failed to write row: %s" % row.values()
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
