#!/usr/bin/python3
import hashlib, binascii, os, json
from binascii import unhexlify
import hashlib
#import pbkdf2
import pbkdf2_ctypes as pbkdf2

USE_PBK = True

#pip3 install pbkdf2-ctypes

#####p.map(add_user, range(2000, 2500))
#####USE_PBK = False
#$ time ./secpassdb.py
#./secpassdb.py  7.02s user 0.41s system 180% cpu 4.110 total
#USE_PBK = True
#$ time ./secpassdb.py
#./secpassdb.py  0.31s user 0.10s system 95% cpu 0.433 total


#https://docs.python.org/3/library/hashlib.html
#####TODO: Note
# A fast implementation of pbkdf2_hmac is available with OpenSSL.
# The Python implementation uses an inline version of hmac.
# It is about three times slower and doesn’t release the GIL.

def unicode_to_bytes(c):
   arr = []
   n = ord(c)
   while n > 254:
      arr.append(254)
      n = n - 254
   arr.append(n)
   return arr

def str_to_bytes(string):
   '''String to bytes

   '''
   bytearr = []
   #for x in bytes(string, 'utf-8'):
   for c in string:
      bytearr = bytearr + unicode_to_bytes(c)
   return bytes(bytearr)

def generate_hash(passw, salt, prepend, n=10000):
   pass_bytes = str_to_bytes(prepend + passw)
   if not USE_PBK:
      dk = hashlib.pbkdf2_hmac('sha256', pass_bytes, str_to_bytes(salt), n)
      return str(binascii.hexlify(dk))
   else:
      dk = pbkdf2.pbkdf2_hex(pass_bytes, str_to_bytes(salt), iterations=n, keylen=24)
      return str(dk)

def generate_salt(salt_len=16):
   return str(binascii.hexlify(os.urandom(salt_len)), 'utf-8')

def generate_prepend(prepend_len=5):
   return str(binascii.hexlify(os.urandom(prepend_len)))


#####USE THIS returns hash json
def gen_pass_hash(password, data_str=None):
   '''Generate has for given password'''
   salt = None
   prepend = None
   #if len(password) < 8:
   #   #raise "Password too short"
   #   return None

   if data_str is None:
      salt = generate_salt()
      prepend = generate_prepend()
      data = {
         'salt' : salt,
         'prepend' : prepend
      }
   else:
      data = json.loads(data_str)
      salt = data['salt']
      prepend = data['prepend']
   data['hash'] = generate_hash(password, salt, prepend)
   #print('hash_data: ' + json.dumps(data))
   return json.dumps(data)

#####USE THIS
def check_pass_match(pass_str_input, hash_json_str):
   '''Check if given password matches hash'''
   origin_data = json.loads(hash_json_str)
   new_hash_str = gen_pass_hash(pass_str_input, hash_json_str)
   if new_hash_str is None:
      return None
   new_json = json.loads(new_hash_str)
   return origin_data['hash'] == new_json['hash']

#dk = hashlib.pbkdf2_hmac('sha256', b'password', b'salt', 10000)
#good = binascii.hexlify(dk)
#print(good)

if __name__ == '__main__':
   passw = 'strong password'
   hash_data = gen_pass_hash(passw)
   print(check_pass_match('another strong password', hash_data))
   print(check_pass_match('strong password', hash_data))

