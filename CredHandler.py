import getpass
import base64
import pickle
from Crypto.Cipher import AES
from Crypto import Random

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class Credhandler(object):

    def __init__(self):
        pass

    def generate(self):
        
        # Generate AES encrypted pickle with input
        
        cred_filename = raw_input('Input the local API credential filename here:')
        cred_list = None
        
        try:
            with open(cred_filename, 'rb') as f:
                cred_data = f.readlines()
                for line in cred_data:
                    try:
                        cred_temp = line.split('=')[1]
                    except:
                        print "Bad credential for API authentication"
                
                    if cred_list is None:
                        cred_list = []
                    cred_list.append(cred_temp.strip(' \t\n\r'))
            print "Local credential loaded"
        except:
            print "Unable to retrieve local credential"
        
        try:
            print "Please provide filename and password for credential pickle generation"
            pickle_filename = raw_input('Input filename for credential pickle:')
            password = pad(getpass.getpass())
            iv = Random.new().read(AES.block_size)
            cred_pickle = pad(pickle.dumps(cred_list))
            encryption_suite = AES.new(password, AES.MODE_CBC, iv)
            cred_pickle_encrypted = encryption_suite.encrypt(cred_pickle)
            f = open(pickle_filename, 'wb')
            f.write(iv+cred_pickle_encrypted)
            f.close()
            print "Encrypted credential saved as:", pickle_filename
        except:
            print "Unable to save encrypted credential pickle"

    def load(self, cred_pickle=None):

        # Load encrypted credential pickle
        cred_list = None
        
        if cred_pickle is None:
            pickle_filename = raw_input('Input filename for credential pickle:')
        password = pad(getpass.getpass())
        try:
            f = open(pickle_filename, 'rb')
            cipher_text = f.read()
            iv = cipher_text[:16]
            encryption_suite = AES.new(password, AES.MODE_CBC, iv)
            cred_pickle = unpad(encryption_suite.decrypt(cipher_text[16:]))
            cred_list = pickle.loads(cred_pickle)
        except:
            print "Unable to load encrypted crendential pickle"

        return cred_list



if __name__ == "__main__":
    keygen = Credhandler()
    keygen.generate()
    keygen.load()
