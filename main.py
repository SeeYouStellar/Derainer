from flask import Flask, render_template, request, redirect, url_for, Response
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome-1')
def welcome_1():
    return render_template('welcome-1.html')

@app.route('/welcome-2')
def welcome2_():
    return render_template('welcome-2.html')

@app.route('/form-step')
def form_step():
    return render_template('form-step.html')

#处理上传的数据集压缩文件
@app.route('/upload-file', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        upload_path = os.path.join(basepath, 'static/upload')
        # 判断文件夹是否存在
        if not os.path.exists(upload_path):
            os.mkdir(upload_path)

        file_path = str(f.filename)
        save_path = upload_path + "/" + file_path
        f.save(save_path)
        print('upload dataset success')
        print(f.filename + ' uploaded at static/upload')

        os.system("unzip " + save_path + ' -d ' + "/opt/web_python/static/api")
        # os.system("/opt/plite-vi/plite-test 2")

        # 调用推理api
        # infer_api =
        # os.system('g++ '+infer_api)
        # api接口返回 static/api/table1.json 和 static/api/img
        # data.json 格式如下：
        # {
        #   "code": 0,
        #   "msg": "",
        #   "count": 1000,
        #   "data": [
        #     {
        #       "id": 1,
        #       "datasetid": "11111",
        #       "labelid": "褶皱",
        #       "x1": "",
        #       "y1": "",
        #       "x2": "",
        #       "y2": "",
        #       "url": "api/img/1.jpg",
        #       "score": ""
        #     }
        # }

    return Response(json.dumps(file_path), mimetype='application/json')

@app.route('/table')
def table():
    return render_template('table.html')

@app.route('/table2')
def table2():
    return render_template('table2.html')

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/edit')
def edit():
    return render_template('edit.html')

# 处理上传的模型
@app.route('/upload-model', methods = ['POST'])
def upload_model():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        upload_path = os.path.join(basepath, 'static/model')
        # 判断文件夹是否存在
        if not os.path.exists(upload_path):
            os.mkdir(upload_path)

        file_path = str(f.filename)
        save_path = upload_path + "/" + file_path
        f.save(save_path)
        print('upload model success')
        print(f.filename + ' uploaded at static/model')

    return Response(json.dumps(file_path), mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)