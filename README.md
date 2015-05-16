# CompanyRankingSystem

Analyzing and visualizing career data to predict company performance with data magic

“There is a treasure hunt under way, driven by the insights to be extracted from data and the dormant value that can be unleashed by a shift from causation to correlation.” - Viktor Mayer-Schönberger

#### Dependencies required:

python-linkedin:
	
	https://github.com/ozgur/python-linkedin

pycrypto:
	
	https://pypi.python.org/pypi/pycrypto

python-crunchbase:

	https://github.com/anglinb/python-crunchbase

#### API credential management:

CompanyRankingSystem provides two ways of credential management, with local .conf file or shared .p file

.conf file can be edited and loaded in plaintext with api authentication credential

.p file is AES encrypted pickle file for credential storage and share. To use .p file for authentication, you may use CredHandler.generate() to generate a .p file with .conf credential file and a password. Once .p file is ready, you would be able to share the .p file and password with someone working together with your project
