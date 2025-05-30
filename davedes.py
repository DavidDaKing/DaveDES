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

Key scheduler process for DES algorithm:
    -Key goes through first permutation
    -Key split into two halves
    -Left shift performed on keys then permutation to create a subkey
    -For 16 subkeys...

"""


def main():
    # This is the global, symmetric key.. All encryption and decryption for DES is done through here..
    randomInt = random.getrandbits(56)
    symmetricKey = format(randomInt, '056b')

    print("Here is the generated symmetric key: ", symmetricKey)

    # Additional keys may be generated for double or triple encryption...

if __name__ == "__main__":
    main()
