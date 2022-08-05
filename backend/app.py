from flask import Flask, jsonify, render_template, request , send_from_directory
from flask_cors import CORS
import string
import os, json,sys
import argparse
import zipfile,time


from checklist.editor import Editor
from checklist.test_types import MFT,INV,DIR
from checklist.expect import Expect
from checklist.test_suite import TestSuite
from checklist.perturb import Perturb
import chinesePerturb
from faker import Faker
import numpy as np

import time

editor = Editor(language='chinese')
religionList = ['基督教','犹太教','伊斯兰教','佛教','琐罗亚斯德教','印度教','锡克教','神道教','巴哈教','道教','儒家','耆那教','无神论','不可知论']
editor.add_lexicon('religion',religionList, overwrite=True)
last_name = [ "李", "王", "张", "刘", "陈", "杨", "吴", "黄", "周", "赵", "孙", "徐", "马", "林", "朱", "郭", "胡", "何",
              "高", "梁", "郑", "罗", "许", "曹", "冯", "邓", "谢", "韩", "于", "宋", "葉", "唐", "蔡", "吕", "程", "曾",
              "沈", "蒋", "董", "范", "田", "姚", "袁", "金", "白", "江", "姜", "谭", "丁", "杜", "彭", "方", "汪", "潘",
              "陆", "苏", "任", "钱", "戴", "余", "侯", "石", "廖", "傅", "魏", "贾", "秦", "肖", "龚", "薛",
              "夏", "关", "孟", "崔", "陶", "顾", "严", "毛", "雷", "孔", "阎", "黎", "邱", "邵", "常", "熊", "万", "章",
              "郝", "贺", "尹", "倪", "洪", "汤", "施", "段", "葛", "邢" ]
editor.add_lexicon('religion',last_name, overwrite=True)
faker=Faker('zh_cn')
first_name = list(set([faker.first_name() for i in range(100)]))
first_name_male = list(set([faker.first_name_male() for i in range(50)]))
first_name_female = list(set([faker.first_name_female() for i in range(50)]))
editor.add_lexicon('first_name',first_name, overwrite=True)
editor.add_lexicon('male',first_name_male, overwrite=True)
editor.add_lexicon('female',first_name_female, overwrite=True)

suite=TestSuite()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = r"./uploadFiles"
# CORS(app, resources={r'/*': {'origins': '*'}})
CORS(app)
'''data=request.args.get('keyword')
    print('keyword',data)'''

class zip:
    def get_zip(self,files,zip_name):
        zp=zipfile.ZipFile(zip_name,'w', zipfile.ZIP_DEFLATED)
        for file in files:
            zp.write(file)
        zp.close()
        time.sleep(5)
        print('压缩完成')

def loadSuite():
    tempList = {}
    for testName in suite.tests:
        print(suite.tests[testName].labels, '--labels--')
        print(suite.info[testName], '')
        suite.tests[testName].name = testName
        suite.tests[testName].type = suite.info[testName]['type']
        suite.tests[testName].description = suite.info[testName]['description']
        suite.tests[testName].capability = suite.info[testName]['capability']
        if type(suite.tests[testName].data[0])==type([]):
            isPair=1
        else:
            isPair=0

        tempList[testName] = {'name': suite.tests[testName].name, 'type': suite.tests[testName].type,
                              'data': suite.tests[testName].data,
                              'labels': suite.tests[testName].labels,
                              'capability': suite.tests[testName].capability,
                              'description': suite.tests[testName].description,
                              'isPair': isPair}
    return jsonify(tempList)



# 测试代码
@app.route('/template', methods=['POST', 'GET'])
def template():
    if request.method == 'GET':
        # get请求是网上复制的代码，没修改过，目前只使用POST
        graph = request.read_json("static/data/miserables.json")
        return graph
    if request.method == 'POST':
        data = request.get_json(silent=True)
        if(data['templates']==[]):

            startt=time.time()
            ret = editor.template(data['template'], nsamples=int(data['number'])).data
            endt=time.time()
            print(endt-startt)
            res_dict={}
            for i in range(len(ret)):
                res_dict[str(i)]=ret[i]
            return jsonify(res_dict)
        else:
            tempList=[data['template']]
            for i in data['templates']:
                tempList.append(i['value'])
            ret = editor.template(tempList, nsamples=int(data['number'])).data
            print(ret)
            res_dict={}
            for i in range(len(ret)):
                res_dict[str(i)]=ret[i]
            return jsonify(res_dict)

@app.route('/getSuggestion', methods=['POST'])
def getSuggestion():
    if request.method == 'POST':
        data = request.get_json(silent=True)
        res = editor.suggest(data['template'])[:int(data['number'])]


        res_dict={}
        for i in range(len(res)):
            res_dict[str(i)]=res[i]
        return jsonify(res_dict)

@app.route('/loadLexicons', methods=['POST', 'GET'])
def loadLexicons():
    if request.method == 'GET':
        # get请求是网上复制的代码，没修改过，目前只使用POST
        graph = request.read_json("static/data/miserables.json")
        return graph
    if request.method == 'POST':
        tempDict=dict(editor.lexicons)
        for key in ['country_city','female_from','first_pronoun','last_from','male_from']:
            del(tempDict[key])
        return jsonify(tempDict)
        #return jsonify(res_dict)

@app.route('/addLexicon', methods=['POST'])
def addLexicon():
    if request.method == 'POST':
        data = request.get_json(silent=True)
        print(data['key'])
        print(data['lexiconList'])
        lexiconList=data['lexiconList'].strip().split(' ')
        editor.add_lexicon(data['key'],lexiconList, overwrite=True)

        tempDict=dict(editor.lexicons)
        for key in ['country_city','female_from','first_pronoun','last_from','male_from']:
            del(tempDict[key])
        return jsonify(tempDict)


@app.route('/addTestSuite', methods=['POST'])
def addTestSuite():
    if request.method == 'POST':
        data = request.get_json(silent=True)
        type_=data['type']
        name=data['name']

        capability=data['capability']
        description=data['description']
        sentences=data['sentences']
        value=data['value']
        print(value)
        value.sort()
        print(value,'SORTED')
        finalSentences=[]
        print(data['number'],'number')
        homoNum=data['homoNum']
        generateNum=int(data['generateNum'])
        for index1,i in enumerate(value):
            for index2,j in enumerate(sentences):
                if j['key']==i:
                    print(i,j,index1,index2)
                    finalSentences.append(j['sentence'])

        if type_=='INV' and data['perturbType']== 'addRandomStr':

            # add random string
            def random_string(n):
                return ''.join(np.random.choice([x for x in string.ascii_letters + string.digits], n))

            def random_url(n=6):
                return 'https://t.co/%s' % random_string(n)

            def random_handle(n=6):
                return '@%s' % random_string(n)

            def add_irrelevant(sentence):
                urls_and_handles = [random_url(n=6) for _ in range(int(data['addRandomStrNumber']))] + [random_handle() for _ in range(int(data['addRandomStrNumber']))]
                irrelevant_before = ['@airline '] + urls_and_handles
                irrelevant_after = urls_and_handles
                rets = ['%s %s' % (x, sentence) for x in irrelevant_before]
                rets += ['%s %s' % (sentence, x) for x in irrelevant_after]
                return rets

            t = Perturb.perturb(finalSentences, add_irrelevant, nsamples=500)
            test = INV(t.data)
            suite.add(test, name, capability, description)
        elif type_=='INV' and data['perturbType']=='punctuation':
            for index1,i in enumerate(finalSentences):
                print(chinesePerturb.punctuation(finalSentences[index1]))
                finalSentences[index1] = chinesePerturb.punctuation(finalSentences[index1])
            test = INV(finalSentences)
            suite.add(test, name, capability, description)
        elif type_=='INV' and data['perturbType']=='homophone':
            for index1,i in enumerate(finalSentences):
                tempList=[finalSentences[index1]]
                while len(tempList)<generateNum+1:
                    generateText = chinesePerturb.tokenPerturb(finalSentences[index1])
                    if generateText not in tempList:
                        tempList.append(generateText)
                finalSentences[index1] = tempList

            test = INV(finalSentences)
            suite.add(test, name, capability, description)
        elif type_=='INV' and data['perturbType']=='change_location':
            loc_lexicon = editor.lexicons['city']+editor.lexicons['country']
            for index1,i in enumerate(finalSentences):

                finalSentences[index1] = chinesePerturb.change_location(finalSentences[index1], loc_lexicon)
            test = INV(finalSentences)
            suite.add(test, name, capability, description)


        elif data['number']==1:

            if type_=='MFT':
                test=MFT(finalSentences, labels=int(data['labels']))
                suite.add(test, name, capability, description)

        elif data['number']==2:
            if type_=='MFT':
                tempList=[]
                print('finalSentences',finalSentences)
                for index,sent in enumerate(finalSentences):
                    if index%2==0:
                        tempList.append([finalSentences[index],finalSentences[index+1]])
                print('tempList',tempList)
                test=MFT(tempList, labels=int(data['labels']))
                #MFT有templates参数，默认None，暂时不传入，后续考虑增加功能
                suite.add(test,name,capability,description)
            elif type_=='DIR':
                if data['direction']=='increasing':
                    monotonic_label=Expect.monotonic(increasing=True,tolerance= float(data['tolerance']))
                elif data['direction']=='decreasing':
                    monotonic_label=Expect.monotonic(increasing=False,tolerance= float(data['tolerance']))
                non_neutral_pred = lambda pred, *args, **kwargs: pred != 0.5
                monotonic_label = Expect.slice_pairwise(monotonic_label, non_neutral_pred)
                tempList=[]
                print('finalSentences',finalSentences)
                for index,sent in enumerate(finalSentences):
                    if index%2==0:
                        tempList.append([finalSentences[index],finalSentences[index+1]])
                print('tempList',tempList)
                test=DIR(tempList,monotonic_label)
                print('tolerance:',data['tolerance'])
                suite.add(test,name,capability,description)
            elif type_ == 'INV':
                tempList = []
                for index, sent in enumerate(finalSentences):
                    if index % 2 == 0:
                        tempList.append([finalSentences[index], finalSentences[index + 1]])
                test = INV(tempList)
                suite.add(test, name, capability, description)


        tempList=loadSuite()
        return tempList

@app.route('/downloadSuite', methods=['POST'])
def downloadSuite():
    suite.to_raw_file('test.txt',n=500,seed=1)
    suite.save('suite.pkl')
    z=zip()
    files=['./test.txt','./suite.pkl']
    # 压缩包路径及名字
    zip_file = './suite.zip'
    z.get_zip(files,zip_file)

    root_path = ''
    src_name = "suite.zip"
    upload_path = os.path.join(root_path, src_name)
    print("upload_path =", upload_path)
    if os.path.isfile(upload_path):
        response = send_from_directory(root_path, src_name, as_attachment=True)
        print("response: ", response)

        response.headers["Access-Control-Expose-Headers"] = "Content-disposition"
        print("response: ", response.headers)
        return response

@app.route('/uploadSuite', methods=['POST'])
def uploadSuite():
    if request.method == 'POST':
        file = request.files.get("file")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], "temp.pkl")
        file.save(file_path)
        global suite
        suite = TestSuite.from_file(file_path)
        tempList=loadSuite()
        return tempList

@app.route('/uploadPred', methods=['POST'])
def uploadPred():
    if request.method == 'POST':
        file = request.files.get("file")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], "tempPred")
        file.save(file_path)
        global suite
        suite.run_from_file(file_path, overwrite=True)

        suite.summary()

        output = sys.stdout
        outputfile = open('summary.txt', 'w')
        sys.stdout = outputfile

        suite.summary()

        outputfile.close()
        sys.stdout = output

        tempList=''
        with open('summary.txt','r') as f:
            tempList+=f.read()


        return jsonify(tempList)

'''
@app.route('/loadSentences',methods=['POST'])
def loadSentences():
    if request.method == 'POST':
        tempList=loadSuite()
        return tempList
'''

@app.route('/deleteSuite',methods=['POST'])
def deleteSuite():
    if request.method == 'POST':
        data = request.get_json(silent=True)
        suiteName = data['suiteName']
        suite.remove(suiteName)
        tempList=loadSuite()
        return tempList

if __name__ == '__main__':
    app.run(host='0.0.0.0')
