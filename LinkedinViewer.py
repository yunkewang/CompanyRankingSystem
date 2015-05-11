from linkedin import linkedin
import sys, re
import CredHandler

class Linkedinviewer (object):


    def __init__ (self, cred_list=None):
        self.authentication = None
        self.application = None
        self.cred_list = cred_list


    def authenticate(self, token=None):

        # Authenticate with LinkedIn Oauth 2 Token
        if token is not None:
            self.application = linkedin.LinkedInApplication(token=token)
            return None
        
        # Authenticate with LinkedIn Oauth 1.0a app credential
        else:
            cred_mode = raw_input('Use local credential conf or AES encrypted pickle? (c/p) ')
            if cred_mode == 'c':
                cred_filename = raw_input('Please input local credential conf filename: ')
                self.authenticate_local_conf(cred_filename)
            elif cred_mode == 'p':
                cred_handler = CredHandler.Credhandler()
                self.cred_list = cred_handler.load()
                try:
                    self.authentication = linkedin.LinkedInDeveloperAuthentication(self.cred_list[0], self.cred_list[1], 
                                                                                   self.cred_list[2], self.cred_list[3], 
                                                                                   self.cred_list[4], linkedin.PERMISSIONS.enums.values())
                    self.application = linkedin.LinkedInApplication(self.authentication)
                except:
                    print "Failed to authenticate with LinkedIn"
                    sys.exit()
            else:
                print "Credential mode invalid"
                sys.exit()

        return None


    def authenticate_local_conf(self, cred_filename=None):

        # Authenticate with LinkedIn local credential .conf file
        cred_list = None
        if cred_filename is not None:
            print cred_filename
            try:
                with open(cred_filename, 'r') as f:
                    cred_data = f.readlines()
            except:
                print "Unable to load credential conf file"
                sys.exit()
            
            for line in cred_data:
                try:
                    cred_temp = line.split('=')[1]
                except:
                    print "Bad credentials for LinkedIn api authentication"
                
                if self.cred_list is None:
                    self.cred_list = []
                self.cred_list.append(cred_temp.strip(' \t\n\r'))

        try:
            self.authentication = linkedin.LinkedInDeveloperAuthentication(self.cred_list[0], self.cred_list[1], self.cred_list[2],
                                                        self.cred_list[3], self.cred_list[4], linkedin.PERMISSIONS.enums.values())
            self.application = application = linkedin.LinkedInApplication(self.authentication)
        except (Exception), ex:
            print "Failed to authenticate with LinkedIn: %s" % ex.message
            sys.exit()

        return None


    def retrieve_profile(self, member_id=None, selectors=None):
        
        # Get profile information
        profile = None

        if member_id is not None:
            profile = self.application.get_profile(member_id=member_id, selectors=selectors)
        else:
            profile = self.application.get_profile(selectors=selectors)
        
        print profile

        return profile


    def retrieve_company(self, company_ids=None, universal_names=None, selectors=None):

        # Get company information
        companies = None
        company_temp = None
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
                except (Exception), ex:
                    print "Unable to retrieve company id: %s, error: %s" % (company_id, ex.message)
                    if len(re.findall('Throttle limit', ex.message)) > 0:
                        sys.exit()

        if universal_names is not None:
            for universal_name in universal_names:
                try:
                    company_temp = self.application.get_companies(universal_names=[universal_name], selectors=selectors)
                    if companies is None:
                        companies = {}
                        companies['values'] = []
                    companies['values'].append(company_temp['values'][0])
                    count = count + 1
                except (Exception), ex:
                    print "Unable to retrieve universal name: %s, error: %s" % (universal_name, ex.message)
                    if len(re.findall('Throttle limit', ex.message)) > 0:
                        sys.exit()

        if count > 0:
            companies['_total'] = count
            # for company in companies['values']:
            #     print '========================\n'
            #     print company
            #     print '\n========================'
        else:
            print "No company retrieved"
            return None

        return companies


    def retrieve_company_updates(self, companies=None, count=1):

        # Get company updates
        company_list = None
        company_updates_dict = None
        
        if companies is not None:
            try:
                for i in range(companies['_total']):
                    if company_list is None:
                        company_list = []
                    company_list.append(companies['values'][i])
                for company in company_list:
                    if company_updates_dict is None:
                        company_updates_dict = {}
                    company_updates_dict[company['name']] = self.application.get_company_updates(company['id'], params={'count': count})
                # for company_name, company_updates in company_updates_dict.iteritems():
                #     print '\n************************', company_name, '************************\n'
                #     for i in range(company_updates['_count']):
                #         print '========================\n'
                #         print company_updates['values'][i]
                #         print '\n========================'
            except (Exception), ex:
                print 'Unable to retrieve company updates: %s' % ex.message
                if re.findall('Throttle limit', ex.message) is not None:
                    sys.exit()
                return None

        return company_updates_dict


if __name__ == "__main__":
    profile_selectors = ['id', 'location', 'first-name', 
                         'last-name', 'industry', 'positions', 
                         'specialties', 'summary'
                        ]
    company_selectors = ['id', 'name', 'company-type', 'stock-exchange', 
                         'ticker', 'industries', 'employee-count-range',
                         'locations', 'founded-year', 'num-followers',
                         'description'
                        ]
    lviewer = Linkedinviewer()
    lviewer.authenticate()
    # lviewer.retrieve_profile(selectors=profile_selectors)
    companies = lviewer.retrieve_company(universal_names=['splunk', 'apple'], selectors=company_selectors)
    # company_updates_dict = lviewer.retrieve_company_updates(companies=companies, count=3)
