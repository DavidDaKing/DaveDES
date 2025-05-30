"""
Source code for DaveDES.py
"""
import bitstring
from bitstring import BitArray
import time
import random

"""
Global Variables here
"""

# Key Permutation 1 array

keyPerm1 = [57, 49, 41, 33, 25, 17, 9,
               1,   58,    50,   42,    34,    26,   18,
              10,    2,    59,   51,    43,    35,   27,
              19,   11,     3,   60,    52,    44,   36,
              63,   55,    47,   39,    31,    23,   15,
               7,   62,    54,   46,    38,    30,   22,
              14,    6,    61,   53,    45,    37,   29,
              21,   13,     5,   28,    20,    12,    4]

"""
I want to start the source code off with the key.

In later versions of this program, I want the user to have the ability to write their own 56 bit keys. For now, I would ask the program to 
generate one randomly. Additionally, I would exclude the weak keys associated with DES encryption. 

Weak keys are keys that produce the same value with the permutation steps in this algorithm.

Key scheduler process for DES algorithm:
    -Key goes through first permutation
    -Key split into two halves
    -Left shift performed on keys then permutation to create a subkey
    -For 16 subkeys...

"""

"""
First permutation function for the key scheduler:
    - I want to permutate with respect to the array keyPerm1
"""
def firstPermKS(key):
    permKey = []
    retKey = [] #key returned to main

    permKey = [key[i] for i in keyPerm1]

    return permKey

def splitArray(key):
    mid = len(key) // 2
    first = key[:mid]
    second = key[mid:]
    return first, second

def keyScheduler(key):
    #Through first permutation
    permKey = firstPermKS(key)
    #Split the key in half
    c0, d0 = splitArray(permKey)
    print(len(permKey))
    print(len(c0))
    

def main():
    # This is the global, symmetric key.. All encryption and decryption for DES is done through here..
    # assinged 64 bits - 5/30
    randomInt = random.getrandbits(64)
    symmetricKey = format(randomInt, '064b')

    print("Here is the generated symmetric key: ", symmetricKey)

    # Additional keys may be generated for double or triple encryption...
    # calling key scheduler
    keyScheduler(symmetricKey)

if __name__ == "__main__":
    main()
