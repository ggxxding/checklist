import re

def punctuation(text):
    tempList = [text]
    if text[-1] == '。':
        tempList.append(text[:-1] + '？')
    elif text[-1] == '？':
        tempList.append(text[:-1] + '。')
    tempList.append(text[:-1] + '、')
    tempList.append(text[:-1] + '，')
    return tempList