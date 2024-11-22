from flask import Flask, render_template, request, redirect
import threading
import time
import os

app = Flask(__name__)


@app.route('/upload', methods=["GET", "POST"])
def upload():
    print('threading.get_ident()', threading.get_ident())
    time.sleep(2)
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        print('request', request)
        print('request => form', request.form)
        print('request => form => name', request.form.get('name'), '、', request.form.get('file_name'))
        print('request => files', request.files.get('file_name'))
        print('request => url', request.url)
        file = request.files.get('file_name')
        # return redirect('/new_path') # 根据 code 不同可以设置，是否要保留当前的一些请求信息。
    return 'upload'


@app.route('/dump', methods=['GET', 'POST'])
def dump_file():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        file_storage = request.files.get('file')
        file = file_storage.stream.read()
        file_name = request.form.get('file_name')
        file_suffix = os.path.splitext(file_storage.filename)[1]
        with open(file_name + file_suffix, 'wb') as f:
            f.write(file)
        print(file_storage.filename)
        print(file)
    return 'dump'


@app.route('/new_path', methods=['GET', 'POST'])
def new_path():
    print('threading.get_ident()', threading.get_ident())

    print('request=>file', request.files)
    if request.method == 'GET':
        return 'new_pth_GET'
    elif request.method == 'POST':
        return 'new_path_POST'


if __name__ == '__main__':
    app.run(port=9099, debug=True)
