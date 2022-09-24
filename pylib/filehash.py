import sys
import hashlib


# Get a file hash of the file
def getfilehash(filepath: str) -> str:
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    md5 = hashlib.md5()
    # sha1 = hashlib.sha1()

    with open(filepath, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
            # sha1.update(data)

    return md5.hexdigest()[:6]
    # print("SHA1: {0}".format(sha1.hexdigest()))