import sys
sys.path.insert(0,'..')
import rsa
(pubkey, privkey) = rsa.newkeys(368)

open('priv.key','w').write(privkey.save_pkcs1())
open('pub.key','w').write(pubkey.save_pkcs1())