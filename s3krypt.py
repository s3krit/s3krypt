#!/usr/bin/python
from optparse import OptionParser
from pprint import pprint
from math import floor
def getmid(seed,e):
    n = pow(seed,e)
    i = int(floor(len(str(n))/2-3))
    return int(str(n)[i:i+6])+1000 # bit hacky. Must be >1000

def xor(pt,key):
    # oh god how did I get here... python's weird
    return "".join([chr(a) for a in [ord(x)^ord(y) for x,y in zip(pt,key)]])

def getseed(string):
    seedtotal = 0
    for char in string:
        seedtotal += ord(char)
    return seedtotal

def permute(pt,key):
    length = len(pt)
    ptList = list(pt)
    for i in range(length):
        swapIndex = ord(key[i])%length
        ptList[i],ptList[swapIndex] = ptList[swapIndex],ptList[i]
    return"".join(ptList)

def unpermute(pt,key):
    length = len(pt)
    ptList = list(pt)
    for i in range(length-1,-1,-1):
        swapIndex = ord(key[i])%length
        ptList[i],ptList[swapIndex] = ptList[swapIndex],ptList[i]
    return"".join(ptList)

def main():
##  Start option parser funtimes
    parser = OptionParser()
    parser.add_option("-k","--keyword",action="store",type="string",dest="keyword")
    parser.add_option("-i","--input",action="store",type="string",dest="infile",default="input.txt")
    parser.add_option("-o","--output",action="store",type="string",dest="outfile",default="output.txt")
    parser.add_option("-d","--decrypt",action="store_true",dest="decrypt")
    parser.add_option("-e","--encrypt",action="store_true",dest="encrypt")
    (options,args) = parser.parse_args()
##  End option parser funtimes

    if options.keyword == None:
        print("ERROR: No keyword given")
        exit(1)
    if options.encrypt and options.decrypt or not(options.encrypt or options.decrypt):
        print("ERROR: Pick either encrypt (-e) or decrypt (-d)")
        exit(1)
    seed = pow(getseed(options.keyword),3)
    infile = open(options.infile,'rb')
    outfile = open(options.outfile,'wb')
    stage0 = bytes.decode(infile.read())
    infile.close()
    key = ""
    while (len(key) < len(stage0)):
        seed = getmid(seed,7)
        key+=chr(seed%128)
    if options.encrypt:
        stage1 = permute(stage0,key)
    else:
        stage1 = stage0
    stage2 = xor(stage1,key)
    if options.decrypt:
        stage3 = unpermute(stage2,key)
    else:
        stage3 = stage2
    outfile.write(str.encode(stage3))
    outfile.close()
    exit(0)

main()
