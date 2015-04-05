import pycrunchbase
import sys
import CredHandler

class Crunchbaseviewer (object):


    def __init__ (self):
        self.authentication = None
        self.application = None


    def authenticate(self):

        # Authenticate with LinkedIn app credential
        cred_mode = raw_input('Use local credential conf or AES encrypted pickle? (c/p) ')
        if cred_mode == 'c':
            cred_filename = raw_input('Please input local credential conf filename: ')
            self.authenticate_local_conf(cred_filename)
        elif cred_mode == 'p':
            cred_handler = CredHandler.Credhandler()
            cred_list = cred_handler.load()
            try:
                self.authenticate = cred_list[0]
                self.application = pycrunchbase.CrunchBase(self.authenticate)
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
                
                if cred_list is None:
                    cred_list = []
                cred_list.append(cred_temp.strip(' \t\n\r'))

        try:
            self.authentication = cred_list[0]
            self.application = pycrunchbase.CrunchBase(self.authenticate)
        except:
            print "Failed to authenticate with LinkedIn"
            sys.exit()

        return None


    def retrieve_profile(self):
        
        # Get profile information

        return None


    def retrieve_company(self, company_ids=None, universal_names=None, selectors=None):

        # Get company information

        return None


    def retrieve_company_updates(self, companies=None, count=1):

        # Get company updates

        return None


if __name__ == "__main__":
    cviewer = Crunchbaseviewer()
    cviewer.authenticate()
    