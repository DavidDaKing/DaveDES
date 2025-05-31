"""
Source code for DaveDES.py
Written by: David Bower
"""
import bitstring
from bitstring import BitArray
import time
import random

"""
Global Variables here
"""

# Key Permutation 1 array
# Questionable formatting, but it works.
keyPerm1 = [57, 49, 41, 33, 25, 17, 9,
               1,   58,    50,   42,    34,    26,   18,
              10,    2,    59,   51,    43,    35,   27,
              19,   11,     3,   60,    52,    44,   36,
              63,   55,    47,   39,    31,    23,   15,
               7,   62,    54,   46,    38,    30,   22,
              14,    6,    61,   53,    45,    37,   29,
              21,   13,     5,   28,    20,    12,    4]

keyPerm2 = [14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32]

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

    permKey = [key[i] for i in keyPerm1]

    return permKey

"""
This function just splits an array into half
"""
def splitArray(key):
    mid = len(key) // 2

    first = key[:mid]
    second = key[mid:]

    return first, second

"""
Left shift helper:
    - Used for all sub keys
    - Amount number as parameter 
"""
def leftShift(key, amount):
    return key[amount:] + key[:amount]

"""
Second Key Permutation:
    - Generates subkeys
"""
def secondPermKS(c, d):
    subKey = []
    subKey += c
    subKey += d
    print(len(c))
    print(len(d))
    print(len(subKey))
    lowKey = [subKey[i] for i in keyPerm2]

    return lowKey

"""
Main key scheduler function:
    -Helper functions defined above
    -I need 16 subkeys with each key being 48-bits long
"""

def keyScheduler(key):
    # Through first permutation
    permKey = firstPermKS(key)

    # Split the key in half
    c0, d0 = splitArray(permKey)

    # Each subkey is based off of each other due to left shift 
    c1 = leftShift(c0, 1)
    d1 = leftShift(d0, 1)
    
    # Create each subkey based off of each other
    c2 = leftShift(c1, 1)
    d2 = leftShift(d1, 1)

    c3 = leftShift(c2, 2)
    d3 = leftShift(d2, 2)

    c4 = leftShift(c3, 2)
    d4 = leftShift(d3, 2)

    c5 = leftShift(c4, 2)
    d5 = leftShift(d4, 2)

    c6 = leftShift(c5, 2)
    d6 = leftShift(d5, 2)

    c7 = leftShift(c6, 2)
    d7 = leftShift(d6, 2)

    c8 = leftShift(c7, 2)
    d8 = leftShift(d7, 2)

    c9 = leftShift(c8, 1)
    d9 = leftShift(d8, 1)

    c10 = leftShift(c9, 2)
    d10 = leftShift(d9, 2)

    c11 = leftShift(c10, 2)
    d11 = leftShift(d10, 2)

    c12 = leftShift(c11, 2)
    d12 = leftShift(d11, 2)

    c13 = leftShift(c12, 2)
    d13 = leftShift(d12, 2)

    c14 = leftShift(c13, 2)
    d14 = leftShift(d13, 2)

    c15 = leftShift(c14, 2)
    d15 = leftShift(d14, 2)

    c16 = leftShift(c15, 1)
    d16 = leftShift(d15, 1)

    # There could've been a faster way of typing it
    # Now that I have all sub keys, I must permutate
    # Kn = perm(Cn, Dn)
    k1 = secondPermKS(c1, d1)
    k2 = secondPermKS(c2, d2)
    k3 = secondPermKS(c3, d3)
    k4 = secondPermKS(c4, d4)
    k5 = secondPermKS(c5, d5)
    k6 = secondPermKS(c6, d6)
    k7 = secondPermKS(c7, d7)
    k8 = secondPermKS(c8, d8)
    k9 = secondPermKS(c9, d9)
    k10 = secondPermKS(c10, d10)
    k11 = secondPermKS(c11, d11)
    k12 = secondPermKS(c12, d12)
    k13 = secondPermKS(c13, d13)
    k14 = secondPermKS(c14, d14)
    k15 = secondPermKS(c15, d15)
    k16 = secondPermKS(c16, d16)
    # You gotta do what you gotta do

    return k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12,k13,k14,k15,k16

def main():
    # This is the global, symmetric key.. All encryption and decryption for DES is done through here..
    # assinged 64 bits - 5/30
    randomInt = random.getrandbits(64)
    symmetricKey = format(randomInt, '064b')

    print("Here is the generated symmetric key: ", symmetricKey)

    # Additional keys may be generated for double or triple encryption...
    # calling key scheduler
    # subkeys defined here
    k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12,k13,k14,k15,k16 = keyScheduler(symmetricKey)
    print(k13)

if __name__ == "__main__":
    main()
