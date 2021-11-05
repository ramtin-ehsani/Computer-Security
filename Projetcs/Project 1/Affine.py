from EnglishDetect import isEnglish
from textblob import TextBlob

SYMBOLS = """ABCDEFGHIJKLMNOPQRSTUVWXYZ"""


def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b


def ModInverse(a, m):
    if gcd(a, m) != 1:
        return None

    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def getKeyParts(key):
    keyA = key // len(SYMBOLS)
    keyB = key % len(SYMBOLS)
    return keyA, keyB


def decryptMessage(key, message):
    keyA, keyB = getKeyParts(key)
    plaintext = ''
    modInverseOfKeyA = ModInverse(keyA, len(SYMBOLS))

    for symbol in message:
        if symbol in SYMBOLS:
            symIndex = SYMBOLS.find(symbol)
            plaintext += SYMBOLS[(symIndex - keyB) * modInverseOfKeyA % len(SYMBOLS)]
        else:
            plaintext += symbol
    return plaintext


def main(myMessage):
    hackedMessage = hack_Affine(myMessage)

    if hackedMessage is not None:
        print(hackedMessage)
    else:
        print('Affine Failed to hack encryption.')
        print()
    return hackedMessage


def hack_Affine(message):
    print('Hacking Affine...')
    for key in range(len(SYMBOLS) ** 2):
        keyA = getKeyParts(key)[0]
        if gcd(keyA, len(SYMBOLS)) != 1:
            continue

        decryptedText = decryptMessage(key, message)

        if isEnglish(decryptedText):
            print()
            print('Key: %s' % key)
            print()
            return decryptedText
    return None


if __name__ == '__main__':
    myMessage = "Pjo mvvqzo aqnjob qi m pyno gv sgzgmlnjmtopqa iwtipqpwpqgz aqnjob kjobo omaj loppob qz mz " \
                "mlnjmtop qi smnnoh pg qpi zwsobqa ouwqdmlozp ozabynpoh wiqzc m iqsnlo smpjosmpqaml vwzapqgz mzh " \
                "agzdobpoh tmae pg m loppob.".upper()
    cipherText = main(myMessage)
    blob = TextBlob(cipherText)
    if blob.detect_language() != 'en':
        print("Possible Warning: blob not detected")
