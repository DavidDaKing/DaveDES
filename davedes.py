"""
Source code for DaveDES.py
"""
import bitstring
from bitstring import BitArray
import time
import random

"""
I want to start the source code off with the key.

In later versions of this program, I want the user to have the ability to write their own 56 bit keys. For now, I would ask the program to 
generate one randomly. Additionally, I would exclude the weak keys associated with DES encryption. 

Weak keys are keys that produce the same value with the permutation steps in this algorithm. 

"""

# This is the global, symmetric key.. All encryption and decryption for DES is done through here..
randomInt = random.getrandbits(56)
symmetricKey = format(randomInt, '056b')

print(symmetricKey)

# Additional keys may be generated for double or triple encryption... 
