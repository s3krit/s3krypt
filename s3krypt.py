from optparse import OptionParser

# Take the seed to the eth power, return middle characters for next iter and seed char
def getmid(seed,e):
    n = pow(seed,e)
    return int(str(n)[4:15])+1000

# The fantastic 1-line xor. Praise be to python!
# iter over each char of the key and pt, xor their ord() and return their chr()
def xor(pt,key):
    return "".join([chr(a) for a in [ord(x)^ord(y) for x,y in zip(pt,key)]])

# calculate initial seed as the sum of chars
def getseed(string):
    seedtotal = 0
    for char in string:
        seedtotal += ord(char)
    return seedtotal

# permute operation - essentially swap pt[i] with pt[key[i]], but tweak key[i] a bit first.
def permute(pt,key):
    length = len(pt)
    ptList = list(pt)
    for i in range(length):
# gotta make sure key[i]'s longer than 127
# but smaller than len(pt), so we square and modulus it
        swapIndex = pow(ord(key[i]),2)%length
        ptList[i],ptList[swapIndex] = ptList[swapIndex],ptList[i]
# classy way to return a list as a string
    return"".join(ptList)

# same as permute but backwards
def unpermute(pt,key):
    length = len(pt)
    ptList = list(pt)
    for i in range(length-1,-1,-1):
        swapIndex = pow(ord(key[i]),2)%length
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
# cool story - comment out the following if clause
# and you get a simple xor if you don't specify -e or -d
    if options.encrypt and options.decrypt or not(options.encrypt or options.decrypt):
        print("ERROR: Pick either encrypt (-e) or decrypt (-d)")
        exit(1)
    seed = pow(getseed(options.keyword),3)

# must open files as binary data, or python3 does weird things to it
    infile = open(options.infile,'rb')
    outfile = open(options.outfile,'wb')
    stage0 = bytes.decode(infile.read())
    infile.close()
    key = ""
    while (len(key) < len(stage0)):
# get new seed and append current (mod 128) to key, as character
        seed = getmid(seed,2)
        key+=chr(seed%128)

# gotta permute then xor if enc
    if options.encrypt:
        stage1 = permute(stage0,key)
    else:
        stage1 = stage0
    stage2 = xor(stage1,key)
# or xor the unpermute if dec
    if options.decrypt:
        stage3 = unpermute(stage2,key)
    else:
        stage3 = stage2
    outfile.write(str.encode(stage3))
    outfile.close()
    exit(0)

# what good is all that fun stuff if you don't call main?
main()
