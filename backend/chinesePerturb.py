import re
import random
from Pinyin2Hanzi import DefaultDagParams
from Pinyin2Hanzi import dag
from pypinyin import lazy_pinyin
import spacy
nlp=spacy.load('zh_core_web_md')

def punctuation(text):
    tempList = [text]
    if text[-1] == '。':
        tempList.append(text[:-1] + '？')
    elif text[-1] == '？':
        tempList.append(text[:-1] + '。')
    tempList.append(text[:-1] + '、')
    tempList.append(text[:-1] + '，')
    return tempList

def pinyin_2_hanzi(pinyinList):
    dagParams = DefaultDagParams()
    # 10个候选值
    result = dag(dagParams, pinyinList, path_num=10, log=True)
    tempList=[]
    for item in result:
        socre = item.score # 得分
        res = item.path # 转换结果
        print(socre, res)
        tempList.append(res[0])
    return tempList

def is_Chinese(ch):
    if '\u4e00' <= ch <= '\u9fff':
        return True
    return False

def tokenPerturb(text, homophoneNum = 1):
    pinyinList=lazy_pinyin(text, errors = lambda x:[y for y in x])
    print(text)
    print(pinyinList)


    chineseNum=0
    for token in text:
        if is_Chinese(token):
            chineseNum+=1
    if chineseNum<homophoneNum:
        print('汉字数量少于生成错别字数量')
        return
    indexList = range(len(pinyinList))
    perturbedIndex = []
    while len(perturbedIndex) <homophoneNum:
        index = random.sample(indexList,1)[0]
        if is_Chinese(text[index]) and index not in perturbedIndex:
            perturbedIndex.append(index)
            tokenList = pinyin_2_hanzi([pinyinList[index]])
            while True:
                token = random.choice(tokenList)
                if token != text[index]:
                    text = text[:index] + token + text[index+1:]
                break

    return text
def change_location(text, loc_lexicon):
    tokens = nlp(text)
    tempText=''
    for token in tokens:
        if token.ent_type_ == 'GPE':
            tempText += random.choice( loc_lexicon )
        else:
            tempText += str(token)
    return tempText




if __name__ == '__main__':
    lists = ['wo', 'you', 'yi', 'zhi', 'xiao', 'mao', 'lv']
    pinyin_2_hanzi(lists)
    tokenPerturb('我有。')