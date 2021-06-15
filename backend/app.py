from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import os, json
import argparse

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


# 测试代码
@app.route('/template', methods=['POST', 'GET'])
def template():
    if request.method == 'GET':
        # get请求是网上复制的代码，没修改过，目前只使用POST
        graph = request.read_json("static/data/miserables.json")
        return graph
    if request.method == 'POST':
        data = request.get_json(silent=True)
        print(data['template'])
        ret = editor.template(data['template'])
        res = np.random.choice(ret.data, int(data['number']))
        print(res)
        res_dict={}
        for i in range(len(res)):
            res_dict[str(i)]=res[i]
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
        if type_=='MFT':
            print(sentences)
            print(type(sentences))

        return jsonify(tempDict)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
