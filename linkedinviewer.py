from linkedin import linkedin
import oauthlib

class Linkedinviewer (object):

	def __init__ (self, cred_file):
		self.cred_file = cred_file
		self.authentication = None
		self.application = None

	def authenticate(self):

		# Define CONSUMER_KEY, CONSUMER_SECRET,  
		# USER_TOKEN, and USER_SECRET from the credentials 
		# provided in your LinkedIn application

		cred_list = []
		with open(self.cred_file, 'r') as f:
			cred_data = f.readlines()
			for line in cred_data:
				try:
					cred_temp = line.split('=')[1]
				except:
					print "Bad credentials for LinkedIn api authentication"
				cred_list.append(cred_temp.strip(' \t\n\r'))

		# Authenticating with LinkedIn

		try:
			self.authentication = linkedin.LinkedInDeveloperAuthentication(cred_list[0], cred_list[1], cred_list[2],
														cred_list[3], cred_list[4], linkedin.PERMISSIONS.enums.values())
			self.application = application = linkedin.LinkedInApplication(self.authentication)
		except:
			print "Failed to authenticate with LinkedIn"


	def get_profile(self):
		
		# Get profile information
		profile = self.application.get_profile()
		print profile

		return profile

	def get_company(self, company_id=None, universal_names=[]):

		# Get company information
		companies = self.application.get_companies(company_id, universal_names)
		print companies

		return companies

	def get_company_updates(self, company_id=None, count=1):

		# Get company updates
		company_updates = self.application.get_company_updates(company_id, params={'count': count})
		print company_updates

		return company_updates

if __name__ == "__main__":
	lviewer = Linkedinviewer('linkedincred.conf')
	lviewer.authenticate()
	lviewer.get_profile()
	companies = lviewer.get_company(universal_names=['splunk'])
	company_list = []
	for i in range(companies['_total']):
		company_list.append(companies['values'][i])
	for company in company_list:
		lviewer.get_company_updates(company_id=company['id'], count=5)