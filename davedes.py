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

# Second Key Permutation array
keyPerm2 = [14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32]

# Initial Permutation Array
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]


# The E expansion table
eExp = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

# The next 8 global arrays are the selection bit tables
s1 = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
]

s2 = [
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
    [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
    [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
    [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
]


s3 = [
    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
    [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
    [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
    [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
]
s4 = [
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
    [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
    [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
    [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
]
s5 = [
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
    [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
    [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
    [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
]
s6 = [
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
    [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
    [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
    [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
]
s7 = [
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
    [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
    [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
    [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
]
s8 = [
    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
    [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
    [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
    [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
]


# 32 bit permutation table
p32 = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]

IPinv = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]
"""
Conversion functions:
    -binary -> decimal
    -decimal -> binary
"""

def bin2Dec(msg):
    return int(msg, 2)

def dec2Bin(num):
    # 2: gets rid of the 0b output
    return bin(num)[2:]

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

    permKey = [key[i-1] for i in keyPerm1]

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

    lowKey = [subKey[i-1] for i in keyPerm2]

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

"""
Key scheduler is over

Onto the DES algorithm for 64 bits/block data 
Below, defines the helper functions to do so. 

DES Algorithm process:
    -The message block goes through Initial Permutation
    -Break in half, goes through XORs and Cipher Functions

"""
# Inital permuation function 
def initPerm(messBlock):
    return [messBlock[i-1] for i in IP]

# Simple XOR function for DES cipher operations on two bit arrays
def XOR(firstArr, secondArr):
    retArr = []
    if len(firstArr) == len(secondArr):
        # Addition operation in the group of mod 2
        for i in range(len(firstArr)):
            if firstArr[i] != secondArr[i]:
                retArr.append(1)
            else:
                retArr.append(0)
        # returning the appended array
        return retArr
    else:
        print("XOR ERROR: Sizes do not match!")


# Expansion function defined here
def expandThis(msg):
    # Takes in 32 bits and expands into 48 bits
    return [msg[i-1] for i in eExp]

# Selection process: takes a 48 bit message
# For each group of 6 bits, the selection table is performed
# G1 -> s1, g2 -> s2 ... g8 -> s8
def selectionProc(msg):
    sMessage = []

    # message groups, 
    m1 = [] 
    m2 = []
    m3 = []
    m4 = []
    m5 = []
    m6 = []
    m7 = []
    m8 = []

    for i in range(0, len(msg), 6):
        if i == 0:
            m1.append(msg[i:i+6])
        if i == 6:
            m2.append(msg[i:i+6])
        if i == 12:
            m3.append(msg[i:i+6])
        if i == 18:
            m4.append(msg[i:i+6])
        if i == 24:
            m5.append(msg[i:i+6])       
        if i == 30:
            m6.append(msg[i:i+6])
        if i == 36:
            m7.append(msg[i:i+6])
        if i == 42:
            m8.append(msg[i:i+6])

    # For some reason, the messages come to a double list
    # I want just a singular list, these lines help with that
    m1 = m1[0]
    m2 = m2[0]
    m3 = m3[0]
    m4 = m4[0]
    m5 = m5[0]
    m6 = m6[0]
    m7 = m7[0]
    m8 = m8[0]

    # For each message list, take the first and last bit
    # Thats the row
    # Take the middle four bits
    # Thats the col

    # Maybe I can use a translator bit -> decimal 
    # Once the translation is done on the S table, append it to
    # S Message

    listOList = [m1, m2, m3, m4, m5, m6, m7, m8]

    listOtab = [s1, s2, s3, s4, s5, s6, s7, s8]

    for i in range(len(listOList)):
        #Stores first and last bits
        bit1 = []
        #Stores middle four
        bit2 = []
        bit1.append(listOList[i][0])
        bit1.append(listOList[i][-1])
        for j in range(1, 5):
            #print(m1[j])
            bit2.append(listOList[i][j])

        # Convert binary -> decimal
        # B1 = row B2 = col
        bit1 = ''.join(map(str,bit1))
        bit2 = ''.join(map(str,bit2))
        dec1 = bin2Dec(bit1)
        dec2 = bin2Dec(bit2)

        # Now that I have row and col vals
        # I will perform the S lookup
        conVal = listOtab[i][dec1][dec2]

        conVal = dec2Bin(conVal).zfill(4)

        # May not be necessary since I fill all with zeros,
        # But if conVal is 0 it fills the rest of the bits w/ zero
        if conVal == 0:
            conVal = [0, 0, 0, 0]

        #conVal = ''.join(map(str,conVal))
        sMessage.append(conVal)
        
    return sMessage

def perm32(msg):
    return [msg[i-1] for i in p32] 

# Cipher function defined here
def cipherFunc(right, key):
    eRight = expandThis(right)

    # Xor the expanded right message w/ the key
    xRight = XOR(eRight, key)

    # Testing expansion function - TEST PASSED
    testRight = [1,1,1,1, 0,0,0,0, 1,0,1,0, 1,0,1,0, 1,1,1,1, 0,0,0,0, 1,0,1,0, 1,0,1,0] 
    expectRight = [0,1,1,1,1,0, 1,0,0,0,0,1, 0,1,0,1,0,1, 0,1,0,1,0,1, 0,1,1,1,1,0, 1,0,0,0,0,1, 0,1,0,1,0,1, 0,1,0,1,0,1]

    testRight = expandThis(testRight)

    #if testRight == expectRight:
        #print("test passed")

    # Testing XOR function - TEST PASSED
    key = [0,0,0,1,1,0, 1,1,0,0,0,0, 0,0,1,0,1,1, 1,0,1,1,1,1, 1,1,1,1,1,1, 0,0,0,1,1,1, 0,0,0,0,0,1, 1,1,0,0,1,0]

    testOut = XOR(testRight, key)
    expOut = [0,1,1,0,0,0, 0,1,0,0,0,1, 0,1,1,1,1,0, 1,1,1,0,1,0, 1,0,0,0,0,1, 1,0,0,1,1,0, 0,1,0,1,0,0, 1,0,0,1,1,1]

    #if testOut == expOut:
        #print("test passed!")

    sRight = selectionProc(xRight)
    #sRight = ''.join(map(str,sRight))
    #print(sRight)

    # Testing S selection process - PASSED

    sTest = selectionProc(testOut)
    #sTest = ''.join(map(str,sTest))
    expS = [0,1,0,1, 1,1,0,0, 1,0,0,0, 0,0,1,0, 1,0,1,1, 0,1,0,1, 1,0,0,1, 0,1,1,1]   
    #expS = ''.join(map(str,expS))

    #if sTest == expS:
        #print("test passed!")
    # Now that the selection process is done, the message needs to
    # Go through a 32-bit permutation
    #sRight = ''.join(map(int,sRight))
    #print(sRight)

    sRight = [int(bit) for binary in sRight for bit in binary]

    sRight = perm32(sRight)

    # Permutation test - PASSED
    #expPerm = [0,0,1,0, 0,0,1,1, 0,1,0,0, 1,0,1,0, 1,0,1,0, 1,0,0,1, 1,0,1,1, 1,0,1,1]
    #sTest = perm32(sTest)
    #sTest = ''.join(map(str,sTest))
    #print(sTest)

    #expPerm = ''.join(map(str,expPerm))

    #if sTest == expPerm:
        #print("test passed")


    return sRight


def invPerm(msg):
    return [msg[i-1] for i in IPinv]



def DES(message, k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13, k14, k15, k16):
    # Init Perm
    messIP = initPerm(message)
    #messIP = ''.join(map(str,messIP))
    #print("initial perm val: ", messIP)

    # Now, split the messIP array in half..
    # Built this function for the keys, but works for message
    # Mr left, mr right: Init LR
    l0, r0 = splitArray(messIP)
    #print("left", l0)
    #print("right", r0)

    # Cipher function!
    l1 = r0
    r1 = XOR(l0, cipherFunc(r0, k1))


    l2 = r1
    r2 = XOR(l1, cipherFunc(r1, k2))

    l3 = r2
    r3 = XOR(l2, cipherFunc(r2, k3))

    l4 = r3
    r4 = XOR(l3, cipherFunc(r3, k4))

    l5 = r4
    r5 = XOR(l4, cipherFunc(r4, k5))

    l6 = r5
    r6 = XOR(l5, cipherFunc(r5, k6))

    l7 = r6
    r7 = XOR(l6, cipherFunc(r6, k7))

    l8 = r7
    r8 = XOR(l7, cipherFunc(r7, k8))

    l9 = r8
    r9 = XOR(l8, cipherFunc(r8, k9))

    l10 = r9
    r10 = XOR(l9, cipherFunc(r9, k10))

    l11 = r10
    r11 = XOR(l10, cipherFunc(r10, k11))

    l12 = r11
    r12 = XOR(l11, cipherFunc(r11, k12))

    l13 = r12
    r13 = XOR(l12, cipherFunc(r12, k13))

    l14 = r13
    r14 = XOR(l13, cipherFunc(r13, k14))

    l15 = r14
    r15 = XOR(l14, cipherFunc(r14, k15))

    l16 = r15
    r16 = XOR(l15, cipherFunc(r15, k16))


    cMes = []
    cMes += r16
    cMes += l16



    # Inverse permutation time
    #cMes = ''.join(map(str, cMes))
    cMes = invPerm(cMes)

    return cMes
    


# Plaintext to hexadecimal conversion for user input
def plainHex(message):
    hexRep = message.encode().hex()
    return hexRep

# Hexadecimal to binary conversion for user input
def hexBin(message):
    binRep = bitstring.BitArray(hex=message)
    binRep = binRep.bin
    return binRep


# Requirements on keys? 

# Pad and split the message
def padSplitMes(message):
    # First pad the message to be multiple of 64 bits
    modChecker = len(message) % 64
    if modChecker != 0:
        toPad = (64 - (len(message) % 64)) % 64
        message = message + '0' * toPad
    return message

def main():


    # Im gonna implement a user loop
    uLoop = 0
    while uLoop != 1:

        # Show options
        print("~~~~~~~~~~~~~")
        print("1 : Run the Simulation")
        print("2 : Encrypt a message with a secret key")
        print("0 : Exit DaveDES")
        print("~~~~~~~~~~~~~")
        uOption = int(input("Enter option here: "))

        if uOption == 0:
            uLoop = 1

        if uOption == 1:
            # This is the global, symmetric key.. All encryption and decryption for DES is done through here..
            # assinged 64 bits - 5/30
            symmetricKey = [0,0,0,1,0,0,1,1,0,0,1,1,0,1,0,0,0,1,0,1,0,1,1,1,0,1,1,1,1,0,0,1,1,0,0,1,1,0,1,1,1,0,1,1,1,1,0,0,1,1,0,1,1,1,1,1,1,1,1,1,0,0,0,1]

            # Additional keys may be generated for double or triple encryption...
            # calling key scheduler
            # subkeys defined here
            k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12,k13,k14,k15,k16 = keyScheduler(symmetricKey)

            listofSub = [k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12,k13,k14,k15,k16]


            # Debugging loop for key scheduler
            # Comment out if you wanna save run time O(n)
            # for i in range(len(listofSub)):
            #      print(f"subkey{i}: {''.join(map(str, listofSub[i]))}")

            # For now the secret message will be pre defined by the computer,
            message = [0,0,0,0, 0,0,0,1, 0,0,1,0, 0,0,1,1, 0,1,0,0, 0,1,0,1, 0,1,1,0, 0,1,1,1, 1,0,0,0, 1,0,0,1, 1,0,1,0, 1,0,1,1, 1,1,0,0, 1,1,0,1, 1,1,1,0, 1,1,1,1]
            #message = ''.join(map(str, message))
            #print("Here is the user message: ", message)

            # I want to build the algorithm first, then add features such as user input, and 3DES. 
            cMes = DES(message, k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13, k14, k15, k16)
    
            print("Encrypted Message", ''.join(map(str,cMes)))

            #Testing purposes: Does it decrypt? - TEST PASSED

            dMes = DES(cMes, k16,k15,k14,k13,k12,k11,k10,k9,k8,k7,k6,k5,k4,k3,k2,k1)

            if dMes == message:
                print("test passed!")


        if uOption == 2:
            uSec = input("Enter a secret key: ")
            hexUSEC = plainHex(uSec)
            uMes = input("Enter the message: ")
            hexUMES = plainHex(uMes)
            # Hex to binary Conversions
            bUSEC = hexBin(hexUSEC)
            bUMES = hexBin(hexUMES)

            # Padding the message for splitting 
            messPad = padSplitMes(bUMES)

            

    

        if uOption != 0 and uOption != 1 and uOption != 2:
            print(f"{uOption} is not an option, try again.")

        # User input section
        """
        User Input: 
            - Translate from plaintext to hexadecimal for both the secret key and the message.
            - Translate from hexadecimal to binary 
        """
        


if __name__ == "__main__":
    main()
