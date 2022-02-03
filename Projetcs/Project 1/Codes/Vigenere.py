import itertools
import re
from FreqAnalysis import MatchScore
from EnglishDetect import isEnglish

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NON_LETTERS = re.compile('[^A-Z]')
MAX_KEY_LENGTH = 16
NUM_MOST_FREQ_LETTERS = 4


def kasiski(ciphertext):
    message = ciphertext
    message = NON_LETTERS.sub('', message.upper())

    seqSpacings = {}
    for seqLen in range(3, 6):
        for seqStart in range(len(message) - seqLen):
            seq = message[seqStart:seqStart + seqLen]

            for i in range(seqStart + seqLen, len(message) - seqLen):
                if message[i:i + seqLen] == seq:
                    if seq not in seqSpacings:
                        seqSpacings[seq] = []

                    seqSpacings[seq].append(i - seqStart)
    repeatedSeqSpacings = seqSpacings

    seqFactors = {}
    for seq in repeatedSeqSpacings:
        seqFactors[seq] = []
        for spacing in repeatedSeqSpacings[seq]:
            seqFactors[seq].extend(UsefulFactors(spacing))

    factorsByCount = getMostCommonFactors(seqFactors)
    allLikelyKeyLengths = []
    for twoIntTuple in factorsByCount:
        allLikelyKeyLengths.append(twoIntTuple[0])

    return allLikelyKeyLengths


def decryptMessage(key, message):
    translated = []

    keyIndex = 0
    key = key.upper()

    for symbol in message:
        num = SYMBOLS.find(symbol.upper())
        if num != -1:
            num -= SYMBOLS.find(key[keyIndex])

            num %= len(SYMBOLS)
            if symbol.isupper():
                translated.append(SYMBOLS[num])
            elif symbol.islower():
                translated.append(SYMBOLS[num].lower())

            keyIndex += 1
            if keyIndex == len(key):
                keyIndex = 0
        else:
            translated.append(symbol)

    return ''.join(translated)


def UsefulFactors(num):
    if num < 2:
        return []

    factors = []
    for i in range(2, MAX_KEY_LENGTH + 1):
        if num % i == 0:
            factors.append(i)
            otherFactor = int(num / i)
            if otherFactor < MAX_KEY_LENGTH + 1 and otherFactor != 1:
                factors.append(otherFactor)
    return list(set(factors))


def getMostCommonFactors(seqFactors):
    factorCounts = {}
    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor not in factorCounts:
                factorCounts[factor] = 0
            factorCounts[factor] += 1
    factorsByCount = []
    for factor in factorCounts:
        if factor <= MAX_KEY_LENGTH:
            factorsByCount.append((factor, factorCounts[factor]))

    factorsByCount.sort(key=IndexOne, reverse=True)

    return factorsByCount


def IndexOne(x):
    return x[1]


def getNthSubkeys(nth, keyLength, message):
    message = NON_LETTERS.sub('', message)

    i = nth - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLength
    return ''.join(letters)


def attemptHack(ciphertext, mostLikelyKeyLength):
    ciphertextUp = ciphertext.upper()

    allFreqScores = []
    for nth in range(1, mostLikelyKeyLength + 1):
        nthLetters = getNthSubkeys(nth, mostLikelyKeyLength, ciphertextUp)
        freqScores = []
        for possibleKey in SYMBOLS:
            decryptedText = decryptMessage(possibleKey, nthLetters)
            keyAndFreqMatchTuple = (possibleKey, MatchScore(decryptedText))
            freqScores.append(keyAndFreqMatchTuple)
        freqScores.sort(key=IndexOne, reverse=True)

        allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])

    for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=mostLikelyKeyLength):
        possibleKey = ''
        for i in range(mostLikelyKeyLength):
            possibleKey += allFreqScores[i][indexes[i]][0]

        decryptedText = decryptMessage(possibleKey, ciphertextUp)

        if isEnglish(decryptedText):
            origCase = []
            for i in range(len(ciphertext)):
                if ciphertext[i].isupper():
                    origCase.append(decryptedText[i].upper())
                else:
                    origCase.append(decryptedText[i].lower())
            decryptedText = ''.join(origCase)
            print('Possible hack with key %s:' % possibleKey)
            return decryptedText

    return None


def hack_Vigenere(ciphertext):
    print('Hacking Vigenere...')
    allLikelyKeyLengths = kasiski(ciphertext)
    keyLengthStr = ''
    for keyLength in allLikelyKeyLengths:
        keyLengthStr += '%s ' % keyLength
    hackedMessage = None
    for keyLength in allLikelyKeyLengths:
        hackedMessage = attemptHack(ciphertext, keyLength)
        if hackedMessage is not None:
            break

    if hackedMessage is None:
        for keyLength in range(1, MAX_KEY_LENGTH + 1):
            if keyLength not in allLikelyKeyLengths:
                print('Attempting hack with key length %s (%s possible keys)...' % (
                    keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
                hackedMessage = attemptHack(ciphertext, keyLength)
                if hackedMessage is not None:
                    break
    return hackedMessage


def main(ciphertext):
    hackedMessage = hack_Vigenere(ciphertext)

    if hackedMessage is not None:
        print(hackedMessage)
    else:
        print('Vigenere Failed to hack encryption.')


if __name__ == '__main__':
    ciphertext = "Lqrserpr Bmlthqq DuFftrur bes nrwr Nayjqbqu 11, 1974 nr Lav Frgqojw, Cmonjodqne, tth trlk fmmlp rk " \
                 "Mryhqmn PlHepdlt enp itvmqu hsmuf gsow dwxiew Liodjj HiOduvia. Knw fmwmir uv tj Ifdqmaz dsh Gquren " \
                 "phxgezw, frd tlx qofkjv, wtr nw Gquren-nrwr, ie rk Kedpfr azg Wyselfr azfjwtdb. Mms ylihlq qfqe, " \
                 "Ilqlexp, bes tlx qafhwrax jwenpifxhqu'x jidvy rayh. Qiozdwho'e ifxhqu med mfmmehhi qizrw wtmwzw ae " \
                 "ds erflxx azg imsfunfufrw sf oxqx capng barp xifojw, azg bes qyjr dqsngtqg nr sqyjvax lxwuqv tj " \
                 "Ayhwmcmq Xtlqqisr, fkj guxw ximu-dzxonltkrmsmmcmo hsmuf gsow vjviqv gc tth qetq 'Kfvvqb Uikmu', " \
                 "f jruhsh or Jjsrsh'x. Peaqfvda'v uirrrwqazfj wkuoqw bqffqe aeamogv ys huv uerqqyw emuqc oz, " \
                 "dsh arwjv sujsmns knq ub znxh m wfpezw fkezw blo idsxep Ojsnmuis ta sjvfaur ynphw xhq vyegq qfqe " \
                 "Xhsry Ilqpimpx, HiOduvia ejkaz dutemunrg aq f ruyejv or wjpehlxmoz ftqmquhmaxv frd qgzgafltrax " \
                 "swsgddrw. "
    main(ciphertext)
