from flask import Flask, render_template, request, url_for, redirect
import json

"""
    知识：
    1、当某个数据既有非JSON数据，也有JSON数据，如果是 get 方法，可以通过 args 获取数据，最后来对获取的数据进行 loads 处理即可。post同理
    2、文件上传，查看项目中的文件上传，都是利用二进制文件，读取文件的内容进行存储，没有使用到 request.file 模块来获取，从接口获取文件目测好像都是利用fast_api 框架。
    3、redirect 可以将调用传入路由路径相应的视图函数，且可以通过配置 code 参数，来判断是否需要保留 HTTP 请求方式 和 请求体，默认 code 不传
        则重新向后的路由采用 GET 请求方式，且不包含旧的请求体。
    4、使用 flask 原生的 request 获取时，当 form-data 格式的数据中包含了 字段 和 文件时，字段可以通过 request.from 来获取
        但文件只能通过 request.files 来获取
        
  
  
    方法：
    1、获取 get 接口数据，使用 args 方法
    2、获取 post 接口数据，使用 form 方法
"""

app = Flask(__name__)


@app.route('/')
def return_html():
    """
    render_template 会在程序运行的同级目录中寻找模板
    """
    return render_template('test.html')


@app.route('/center/add', methods=['GET', 'POST'])
def center():
    """
    methods 为 get：通过request.args 来获取参数
    methods 为 post：通过request.from 来获取参数
    """
    print('request', request)
    if request.method == 'GET':
        print('args', request.args)
        name = request.args.get('name')
        age = request.args.get('age')
        hobby = request.args.getlist('hobby')  # getlist 可以获取多个同名称的字段,相当于接受get参数时的数组。
        # 两种形式：一种是 url 上的多个同名称参数：/center/add?hobby=篮球&hobby=足球&hobby=排球
        # 一种是：在前端的请求体中传入数组，通过actions方法来进行拼接到url上传参
        print('getlist=>hobby', hobby)

    elif request.method == 'POST':
        print('form', request.form)
        name = request.form.get('name')
        age = request.form.get('age')
        hobby = request.form.getlist('hobby')
        print(url_for('new_path'))
        # return redirect(url_for('new_path'), )  # 根据 code 不同可以设置，是否要保留当前的一些请求信息。
    return f'name:{name}、age:{age}、hobby:{hobby}'


@app.route('/new_path', methods=["GET", "POST"])
def new_path():
    name = request.form.get('name')
    age = request.form.get('age')
    hobby = request.form.getlist('hobby')
    print(f'new_path => name:{name}、age:{age}、hobby:{hobby}')
    return 'new_path'


if __name__ == "__main__":
    app.run(port=9091, debug=True)
