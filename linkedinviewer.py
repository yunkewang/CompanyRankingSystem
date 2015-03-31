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

		# Authenticating with LinkedIn

		try:
			self.authentication = linkedin.LinkedInDeveloperAuthentication(cred_list[0], cred_list[1], cred_list[2],
														cred_list[3], cred_list[4], linkedin.PERMISSIONS.enums.values())
			self.application = application = linkedin.LinkedInApplication(self.authentication)
		except:
			print "Failed to authenticate with LinkedIn"

		return None

	def get_profile(self):
		
		# Get profile information
		profile = self.application.get_profile()
		print profile

		return profile

	def get_company(self, company_id=None, universal_names=None):

		# Get company information
		companies = self.application.get_companies(company_id, universal_names)
		print companies

		return companies

	def get_company_updates(self, companies=None, count=1):

		# Get company updates
		company_list = None
		company_updates_dict = None
		
		print 'test'
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
	lviewer.get_profile()
	companies = lviewer.get_company(universal_names=['apple', 'splunk'])
	company_updates_dict = lviewer.get_company_updates(companies=companies, count=3)