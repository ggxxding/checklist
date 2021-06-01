from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import os, json
import argparse

from checklist.editor import Editor
import numpy as np
editor = Editor(language='chinese')

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


@app.route('/uploadFile', methods=['POST'])
def upload():
    if request.method == 'POST':
        # name = request.form.get("name")
        # description = request.form.get("description")
        file = request.files.get("file")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], "temp.json")
        file.save(file_path)
        # print(name)
        # print(description)
        data = json.loads(open(file_path, 'r').read())  # type = dict
        jsondata = {}
        jsondata['article'] = data['article']
        jsondata['options'] = data['options']
        jsondata['answers'] = data['answers']
        # print(data)
        # print(data['article'])
        # print(data['answers'])
        os.remove(file_path)
        return jsondata


@app.route('/clozeTest', methods=['POST'])
def clozeTest():
    if request.method == 'POST':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], "temp.json")
        model = request.form.get("model")
        data = {}
        data["article"] = request.form.get("article")
        data["mask"] = request.form.get("mask")
        tempOps = request.form.get("options").strip()[3:-3]
        tempOps = tempOps.split('"],["')
        for i, j in enumerate(tempOps):
            tempOps[i] = tempOps[i].split('","')
        data["options"] = tempOps
        data["includeAnswer"] = request.form.get("includeAnswer")
        includeAnswer = data["includeAnswer"]
        # 不包含正确答案则不输出准确率
        if (data["includeAnswer"] == "1"):
            tempAns = request.form.get("answers").strip()[2:-2]
            tempAns = tempAns.split('","')
            data["answers"] = tempAns
        json_str = json.dumps(data, indent=4)
        with open(file_path, 'w') as json_file:
            json_file.write(json_str)

        parser = argparse.ArgumentParser()
        args = parser.parse_args()
        args.data_dir = './uploadFiles/'
        args.pre = args.post = 0
        args.bert_model = model
        args.save_name = './data/{}-'.format('valid') + args.bert_model + '.pt'
        args.mask = data["mask"]
        args.includeAnswer = includeAnswer
        data = data_util_bert.Preprocessor(args)

        parser = argparse.ArgumentParser()
        args = parser.parse_args()
        args.data_dir = './data'
        args.bert_model = model
        args.task_name = 'cloth'
        args.output_dir = './output'
        args.do_train = False
        args.do_eval = True
        args.train_batch_size = 4
        args.cache_size = 256
        args.eval_batch_size = 1
        args.learning_rate = 5e-5
        args.num_train_epochs = 3.0
        args.num_log_steps = 10
        args.warmup_proportion = 0.1
        args.no_cuda = False
        args.local_rank = -1
        args.seed = 42
        args.gradient_accumulation_steps = 1
        args.optimize_on_cpu = False
        args.fp16 = False
        args.loss_scale = 128
        args.includeAnswer = includeAnswer

        acc, ans = main_bert.main(args)
        acc = str(acc * 100) + '%'
        data = {'acc': acc, 'ans': ans}

        return data


if __name__ == '__main__':
    app.run(host='0.0.0.0')
