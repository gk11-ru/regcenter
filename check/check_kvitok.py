import sys
sys.path.insert(0,'..')
import rsa, base64, os

def check_keys(msg,key):
    ''' return key name if ok, empty if no '''
    for ck in os.listdir('keys'):
        pubkey =  rsa.PublicKey.load_pkcs1( open('keys/%s' % ck).read() )
        try:
            if rsa.verify(msg,key,pubkey):
                return ck
        except:
            pass
    return ''

data = base64.urlsafe_b64decode(sys.argv[1].strip(':')).splitlines()

dmsg = '%s\n%s\n%s\n' % tuple(data[:3])
dkey = base64.urlsafe_b64decode(data[3])

print check_keys(dmsg,dkey)


