from crunchbase import CrunchBase
import sys, re
import CredHandler

class Crunchbaseviewer (object):


    def __init__ (self):
        self.authentication = None
        self.application = None


    def authenticate(self, token=None):

        # Authenticate with passed-in token
        if token is not None:
            try:
                self.application = CrunchBase(token)
            except (Exception), ex:
                print "Failed to authenticate with CrunchBase: %s" % ex.message
                sys.exit()

        # Authenticate with CrunchBase API credential
        else:
            cred_mode = raw_input('Use local credential conf or AES encrypted pickle? (c/p) ')
            if cred_mode == 'c':
                cred_filename = raw_input('Please input local credential conf filename: ')
                self.authenticate_local_conf(cred_filename)
            elif cred_mode == 'p':
                cred_handler = CredHandler.Credhandler()
                cred_list = cred_handler.load()
                try:
                    self.authentication = cred_list[0]
                    self.application = CrunchBase(self.authentication)
                except (Exception), ex:
                    print "Failed to authenticate with CrunchBase: %s" % ex.message
                    sys.exit()
            else:
                print "Credential mode invalid"
                sys.exit()

        return None


    def authenticate_local_conf(self, cred_filename=None):

        # Authenticate with CrunchBase local credential .conf file
        cred_list = None
        if cred_filename is not None:
            print cred_filename
            try:
                with open(cred_filename, 'r') as f:
                    cred_data = f.readlines()
            except (Exception), ex:
                print "Unable to load credential conf file: %s" % ex.message
                sys.exit()
            
            for line in cred_data:
                try:
                    cred_temp = line.split('=')[1]
                except (Exception), ex:
                    print "Bad credentials for CrunchBase api authentication %s" % ex.message
                
                if cred_list is None:
                    cred_list = []
                cred_list.append(cred_temp.strip(' \t\n\r'))

        try:
            print cred_list[0]
            self.authentication = cred_list[0]
            self.application = CrunchBase(self.authentication)
        except (Exception), ex:
            print "Failed to authenticate with CrunchBase: %s" % ex.message
            sys.exit()

        return None


    def retrieve_profile(self):
        
        # Get profile information

        return None


    def retrieve_company(self, company_name=None, selectors=None):

        # Get company information

        if company_name is not None:
            try:
                company = self.application.getOrganization(company_name)
            except (Exception), ex:
                print "Failed to retrieve company: %s, error: %s" % (company_name, ex.message)
                if len(re.findall('limit', ex.message)) > 0:
                    sys.exit()
                return None

        return company


    def retrieve_company_updates(self, companies=None, count=1):

        # Get company updates

        return None


if __name__ == "__main__":
    cbviewer = Crunchbaseviewer()
    cbviewer.authenticate()
    cbviewer.retrieve_company(company_name='Wetpaint')
    