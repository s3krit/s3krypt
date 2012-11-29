#!/usr/bin/python
from optparse import OptionParser
def getmid(seed,e):
    n = pow(seed,e)
    i = len(str(seed))/2-2
    return int(str(n)[i:i+6])+1000 # bit hacky. Must be >1000

def getcipher(pt,key):
    # oh god how did I get here... python's weird
    return "".join([chr(a) for a in [ord(x)^ord(y) for x,y in zip(pt,key)]])

def getseed(string):
    seedtotal = 0
    for char in string:
        seedtotal += ord(char)
    return seedtotal

def main():
    parser = OptionParser()
    parser.add_option("-k","--keyword",action="store",type="string",dest="keyword")
    parser.add_option("-i","--input",action="store",type="string",dest="infile",default="plaintext")
    parser.add_option("-o","--output",action="store",type="string",dest="outfile",default="ciphertext")
    (options,args) = parser.parse_args()
    if len(options.keyword:
        return 0
    seed = pow(getseed(options.keyword),3)
    ptf = open(options.infile,'r')
    cf = open(options.outfile,'w')
    plaintext = ptf.read()
    plaintext=plaintext[::-1]
    ptf.close()
    key = ""
    while (len(key) < len(plaintext)):
        seed = getmid(seed,5)
        key+=chr(seed%256)
    ciphertext = getcipher(plaintext,key)
    cf.write(ciphertext[::-1])
    cf.close()

main()
