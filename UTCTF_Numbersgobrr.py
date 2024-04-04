#!/usr/bin/env python3

'''
This is the solution to a CTF challenge in the UTCTF
The script exploits an insufficient entropy when generating a pseudorandom number.
'''

ciphertext = '5c990ae1a92acbac80490cea45fa4880179fc0b0cda5b1a076b8f4c6d9b2cff778743e0dbc47604f2d3a871380be7a04'

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

# Encryption is given by the challenge
def get_random_number():
    global seed 
    seed = int(str(seed * seed).zfill(12)[3:9])
    return seed

# The function that decrypts was programmed following the one that encrypts
def decrypt(ciphertext, seed):
    # Given by the callenge
    key = b''
    for i in range(8):
        key += (get_random_number() % (2 ** 16)).to_bytes(2, 'big')
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(bytes.fromhex(ciphertext))
    potFlag = ''
    # Try to decode. If it raises an error, just continue.
    try:
    	potFlag = unpad(decrypted, AES.block_size).decode()
    except:
    	pass
    return potFlag

# Given ciphertext and bruteforcing the seed
for seed in range (1,10**6):
	print ("Trying " + str(seed) + "\r", end = "")
	# Decrypting the ciphertext using the recovered key
	flag = decrypt(ciphertext, seed)
	if(flag != ''):
		with open("flag.txt", "a") as f:
			f.write('\n'+flag + '\n')
		print (flag)
