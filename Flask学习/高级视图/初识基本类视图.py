from flask import Flask, views, render_template

"""
    知识：
    1、类视图简单理解：定义一个类视图，内部需要实现，dispatch_request 方法。
        在进行 app.add_url_rule 时，会将路由路径绑定到 endpoint 中，endpoint 会绑定一个 view_func，view_func 会通过 as_view 
        生成一个视图函数，在 as_view 方法中，内部会生成一个 view 函数，view 函数内部会调用，当前的类对象的 dispatch_request 方法，
        并且会将传入 as_view 的名称修改给 view 函数的名称，并返回 view 函数，所以最终，app.add_url_rule 绑定的时 as_view 传递出的 
        view 函数，view 函数内部会触发 类对象 中的 dispatch_request 方法，以此可以实现 路由 跟 类视图 的映射。
"""


# 继承 View 类，因为 View 类中含有 as_view 方法，到时候可以直接通过实例对象调用该方法。
class Ads(views.View):
    def __init__(self):
        self.context = {
            'ads': '这是一个广告'
        }


class Index(Ads):
    methods = ["GET", "POST"]

    def __init__(self):
        super(Index, self).__init__()

    # 类视图匹配到对应路径实际调用的方法。
    def dispatch_request(self):
        return render_template('class_module/index.html', **self.context)


class Login(Ads):
    def __init__(self):
        super(Login, self).__init__()

    def dispatch_request(self):
        return render_template('class_module/login.html', **self.context)


class Register(Ads):
    def __init__(self):
        super(Register, self).__init__()

    def dispatch_request(self):
        return render_template('class_module/register.html', **self.context)


app = Flask(__name__)

# as_view 函数内部会返回一个视图，视图内部会调用类对象的 dispatch_request
app.add_url_rule('/', endpoint='index', view_func=Index.as_view('index'))
app.add_url_rule('/login', endpoint='login', view_func=Login.as_view('login'))
app.add_url_rule('/register', endpoint='register', view_func=Register.as_view('register'))

if __name__ == '__main__':
    app.run(port=9099, debug=True)
