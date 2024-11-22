from flask import Flask, views, render_template, request, jsonify

"""
    知识：
    1、MethodView 相当于是 View 的子类，在 View 的基础上再次进行了封装，MethodView 内部实现了 dispatch_reqeust 方法
        在 dispatch_request 方法中，会判断当前请求的方式，根据当前请求的方式转为小写，再去调用实例中相对应的方法，达到在类
        中，定义对应的请求方法，来实现不同的请求方式调用不同的请求方法，如：当请求方式为 POST 时，会转为小写 post ，并保存为
        一个变量 post ，在去调用当前实例中相同名称的方法，self.post，便能达到效果
"""


class Ads(views.MethodView):
    def __init__(self):
        self.context = {
            'ads': '这是一个广告'
        }


class LoginView(Ads):

    def __init__(self):
        super(LoginView, self).__init__()

    def get(self):
        return render_template('index.html', **self.context)

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == '123456':
            return jsonify('success')
        else:
            return jsonify('error')


app = Flask(__name__)

app.add_url_rule('/login', view_func=LoginView.as_view('login'))

if __name__ == '__main__':
    app.run(port=9099)
