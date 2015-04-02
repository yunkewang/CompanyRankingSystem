from linkedin import linkedin
import oauthlib

class Linkedinviewer (object):

    def __init__ (self, cred_file):
        self.cred_file = cred_file
        self.authentication = None
        self.application = None

    def authenticate(self):

        # Authenticate with LinkedIn app credential
        cred_list = None
        with open(self.cred_file, 'r') as f:
            cred_data = f.readlines()
            for line in cred_data:
                try:
                    cred_temp = line.split('=')[1]
                except:
                    print "Bad credentials for LinkedIn api authentication"
                
                if cred_list is None:
                    cred_list = []
                cred_list.append(cred_temp.strip(' \t\n\r'))

        try:
            self.authentication = linkedin.LinkedInDeveloperAuthentication(cred_list[0], cred_list[1], cred_list[2],
                                                        cred_list[3], cred_list[4], linkedin.PERMISSIONS.enums.values())
            self.application = application = linkedin.LinkedInApplication(self.authentication)
        except:
            print "Failed to authenticate with LinkedIn"

        return None

    def retrieve_profile(self):
        
        # Get profile information
        profile = self.application.get_profile()
        print profile

        return profile

    def retrieve_company(self, company_ids=None, universal_names=None, selectors=None):

        # Get company information
        companies = None
        count = 0
        
        if company_ids is not None:
            for company_id in company_ids:
                try:
                    company_temp = self.application.get_companies(company_ids=[company_id], selectors=selectors)
                    if companies is None:
                        companies = {}
                        companies['values'] = []
                    companies['values'].append(company_temp['values'][0])
                    count = count + 1
                except:
                    print "Unable to retrieve company id:", company_id

        if universal_names is not None:
            for universal_name in universal_names:
                try:
                    company_temp = self.application.get_companies(universal_names=[universal_name], selectors=selectors)
                    if companies is None:
                        companies = {}
                        companies['values'] = []
                    companies['values'].append(company_temp['values'][0])
                    count = count + 1
                except:
                    print "Unable to retrieve universal name:", universal_name

        if count > 0:
            companies['_total'] = count
        
        for company in companies['values']:
            print '========================\n'
            print company
            print '\n========================'

        return companies

    def retrieve_company_updates(self, companies=None, count=1):

        # Get company updates
        company_list = None
        company_updates_dict = None
        
        if companies is not None:
            for i in range(companies['_total']):
                if company_list is None:
                    company_list = []
                company_list.append(companies['values'][i])
            for company in company_list:
                if company_updates_dict is None:
                    company_updates_dict = {}
                company_updates_dict[company['name']] = self.application.get_company_updates(company['id'], params={'count': count})
            for company_name, company_updates in company_updates_dict.iteritems():
                print '\n************************', company_name, '************************\n'
                for i in range(company_updates['_count']):
                    print '========================\n'
                    print company_updates['values'][i]
                    print '\n========================'

        return company_updates_dict

if __name__ == "__main__":
    lviewer = Linkedinviewer('linkedincred.conf')
    lviewer.authenticate()
    lviewer.retrieve_profile()
    selectors = ['id', 'name', 'company-type', 'stock-exchange', 
                 'ticker', 'industries', 'employee-count-range',
                 'locations', 'founded-year', 'num-followers'
                ]
    companies = lviewer.retrieve_company(universal_names=['sciencelogic', 'splunk'], selectors=selectors)
    company_updates_dict = lviewer.retrieve_company_updates(companies=companies, count=3)