from flask import Flask, jsonify, render_template, request , send_from_directory
from flask_cors import CORS

import os, json
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
        lexiconList=data['lexiconList'][1:-1].split(',')
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
        labels=data['labels']
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
        if data['number']==1:
            if type_=='MFT':
                test=MFT(finalSentences, labels=labels)
                suite.add(test, name, capability, description)
        elif data['number']==2:
            if type_=='MFT':
                tempList=[]
                print(finalSentences)
                for index,sent in enumerate(finalSentences):
                    if index%2==0:
                        tempList.append([finalSentences[index],finalSentences[index+1]])
                print(tempList)
                test=MFT(tempList, labels=labels)
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


        tempList={}
        for testName in suite.tests:
            print(dir(suite.tests[testName]))
            print(suite.tests[testName].labels,'--labels--')
            print(suite.info[testName],'')
            suite.tests[testName].name=testName
            suite.tests[testName].type = suite.info[testName]['type']
            suite.tests[testName].description = suite.info[testName]['description']
            suite.tests[testName].capability = suite.info[testName]['capability']
            tempList[testName]={'name':suite.tests[testName].name,'type':suite.tests[testName].type,'data':suite.tests[testName].data,
                                'labels':suite.tests[testName].labels,
                           'capability':suite.tests[testName].capability,'description':suite.tests[testName].description}
        return jsonify(tempList)

@app.route('/downloadSuite', methods=['POST'])
def downloadSuite():
    suite.to_raw_file('test.txt')
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

if __name__ == '__main__':
    app.run(host='0.0.0.0')
