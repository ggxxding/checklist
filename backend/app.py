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
import numpy as np

editor = Editor(language='chinese')
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
            ret = editor.template(data['template'], nsamples=int(data['number'])).data
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

        finalSentences=[]
        print(data['number'],'number')
        for index1,i in enumerate(value):
            for index2,j in enumerate(sentences):
                if j['key']==i:
                    print(i,j,index1,index2)
                    finalSentences.append(j['sentence'])

        if data['addRandomStr']==True:

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
        elif data['number']==1:

            if type_=='MFT':
                test=MFT(finalSentences, labels=int(data['labels']))
                suite.add(test, name, capability, description)

        elif data['number']==2:
            if type_=='MFT':
                tempList=[]
                print(finalSentences)
                for index,sent in enumerate(finalSentences):
                    if index%2==0:
                        tempList.append([finalSentences[index],finalSentences[index+1]])
                print(tempList)
                test=MFT(tempList, labels=int(data['labels']))
                #MFT有templates参数，默认None，暂时不传入，后续考虑增加功能
                suite.add(test,name,capability,description)
            elif type_=='DIR':
                if data['direction']=='increasing':
                    monotonic_label=Expect.monotonic(increasing=True,tolerance= float(data['tolerance']))
                elif data['direction']=='decreasing':
                    monotonic_label=Expect.monotonic(increasing=False,tolerance= float(data['tolerance']))
                non_neutral_pred = lambda pred, *args, **kwargs: pred != 1
                monotonic_label = Expect.slice_pairwise(monotonic_label, non_neutral_pred)
                tempList=[]
                for index,sent in enumerate(finalSentences):
                    if index%2==0:
                        tempList.append([finalSentences[index],finalSentences[index+1]])
                test=DIR(tempList,monotonic_label)
                print(data['tolerance'])
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
@app.route('/loadSentences',methods=['POST'])
def loadSentences():
    if request.method == 'POST':
        tempList=loadSuite()
        return tempList

if __name__ == '__main__':
    app.run(host='0.0.0.0')
