from LinkedinViewer import Linkedinviewer
#import CrunchbaseViewer
from pymongo import MongoClient
import csv

class Dataintegrator(object):

    def __init__(self):
        
        self.lviewer = Linkedinviewer()
        self.mongo_client = MongoClient()
        self.db = None
        self.collection = None
        self.input_data = []
        self.company_selectors = ['id', 'name', 'company-type', 'stock-exchange', 
                                  'ticker', 'industries', 'employee-count-range',
                                  'locations', 'founded-year', 'num-followers',
                                  'description'
                                 ]

        return None

    
    def pre_process(self):
        """
        Get LinkedIn API authenticated and MongoDB collection ready for data integration
        """
        self.lviewer.authenticate()
        db_name = raw_input('Input name of db: ')
        collection_name = raw_input('Input name of collection: ')
        csv_filename = raw_input('Input name of csv file: ')
        if db_name is not None and collection_name is not None and csv_filename is not None:
            self.db = self.mongo_client[db_name]
            self.collection = self.db[collection_name]
            try:
                with open(csv_filename, 'rb') as f:
                    try:
                        for input_dict in csv.DictReader(f):
                            self.input_data.append(input_dict)
                    except (Exception), ex:
                        print "Failed to convert csv data: %s" % ex.message
            except (Exception), ex:
                print "Failed to import from csv %s: %s" % (csv_filename, ex.message)
        
        return None


    def process(self):
        """
        Get data from LinkedIn and merge data into MongoDB
        """
        countdown = 50
        if len(self.input_data) > 0:
            for company in self.input_data:
                try:
                    company_name_origin = company['name']
                    company_name_linkedin = company_name_origin.lower().replace(" ", "-")
                    company_profile = self.lviewer.retrieve_company(universal_names=[company_name_linkedin],
                                                                    selectors=self.company_selectors)
                    countdown = countdown - 1
                    if company_profile is not None and len(company_profile) > 0:
                        company['linkedin_profile'] = company_profile['values'][0]
                        self.collection.insert(company)
                except (Exception), ex:
                    print "Failed to retrieve company profile and save: %s" % ex.message
                if countdown == 0:
                    self.lviewer.authenticate()
                    countdown = 50


if __name__ == '__main__':
    di = Dataintegrator()
    di.pre_process()
    di.process()