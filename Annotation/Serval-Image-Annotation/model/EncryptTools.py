import base64
from hashlib import md5
from config import defaults as DEF

def encrypt(key, clear):
    if len(key)==0:
        return clear
    enc = []
    if not isinstance(clear, bytes):
        clear = clear.encode('utf-8')
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = (clear[i] + ord(key_c)) % 256
        enc.append(enc_c)
    enc = bytes(enc)
    return base64.standard_b64encode(enc).decode()


def decrypt(key, enc):
    if len(key)==0:
        return enc
    dec = []
    enc = base64.standard_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = (256 + enc[i] - ord(key_c)) % 256
        dec.append(dec_c)
    return bytes(dec).decode('utf-8')

def addHeader(annotationLines:str):
    bytes=annotationLines.encode('utf-8')
    hash_bytes=md5(bytes).hexdigest()
    #print(type(hash_bytes))
    topline=DEF.SERVAL_HEADER_PREFIX_IMAGE+hash_bytes
    return topline+'\n'+annotationLines

def validateHeader(annotationLinesWithHeader:str):
    topLine=annotationLinesWithHeader.split('\n')[0]
    print(topLine)
    if not topLine.startswith(DEF.SERVAL_HEADER_PREFIX_IMAGE):
        print("invalid prefix")
        return 1
    print(len(topLine[8:]))
    md5sum=topLine[8:]
    print(md5sum)
    annotationLinesList = annotationLinesWithHeader.split('\n')[1:]
    annotationLines='\n'.join(annotationLinesList)
    #print(annotationLines)
    hash=md5(annotationLines.encode('utf-8')).hexdigest()
    print(hash)
    if hash==md5sum:
        print("valid")
        return 0
    else:
        print("invalid")
        return 2
if __name__=="__main__":
    with open('zip.serval',encoding='utf-8') as f:
        str_serval=f.read()
    str_decrypt=decrypt(DEF.ENCRYPT_KEY,str_serval)
    print(str_decrypt)
    with open('decrypt.serval','w',encoding='utf-8') as f_write:
        f_write.write(str_decrypt)
    validateHeader(str_decrypt)
    annotationLinesList = str_decrypt.split('\n')[1:]
    annotationLines = '\n'.join(annotationLinesList)
    getHeader=addHeader(annotationLines)
    #print(getHeader)
    codec=encrypt(DEF.ENCRYPT_KEY,getHeader)
    print(type(codec))


