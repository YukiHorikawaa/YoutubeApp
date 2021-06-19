import unicodedata
import KeyEnum 
import re

f = open('sample/application/wordstudy.txt', 'r')
text = f.read()
print(text)
print("------------------------------------------------------------------\n")

def reshapetext(text):
    # tables = ['\u3000','　',' ','\x0c','\x0b','\t','\n','\r']
    tables = ['\u3000','\x0c','\x0b','\t','\n','\r']
    table = str.maketrans({
    v: '' for v in tables
    })
    text = text.translate(table)
    # text = ''.join(text.splitlines())
    # text = re.sub(r"\s", "", text)
    text = text.replace("\\"+"n","")
    print(text)
    print("------------------------------------------------------------------\n")
    return text

def calc(text, word, key = -1):
    try:
        reshapetext(text)
        count = 0
        countNum = 0
        maxWord = 0
        if key == KeyEnum.KeyNum.TITLE:
            maxWord = 60
        elif key == KeyEnum.KeyNum.DESCRIPTION:
            maxWord = 200
        else:
            maxWord = 0

        for c in text:
            print(c)
            if unicodedata.east_asian_width(c) in 'FWA':
                count += 1
                countNum += 1
            elif c == " ":
                countNum += 1
                print('CONTINUE')
                continue
            # elif unicodedata.east_asian_width(c) in ["Na", "H", "N"]:
            else:    
                count += 0.5
                countNum += 1
            
            if  maxWord != 0 and count >= maxWord:
                text = text[0:countNum]
                break
        print(text)
        print("------------------------------------------------------------------\n")
        Len = len(text)
        Place = text.find(word) if text.find(word) != -1 else 0
        Rate = (1 - (Place/Len+0.0001))*100 if Place != 0 else 0
                
        return Len, Place, Rate

    except IndexError:
        # raise
        print("url error")
        pass

print(calc(text, "RNN", KeyEnum.KeyNum.DESCRIPTION))