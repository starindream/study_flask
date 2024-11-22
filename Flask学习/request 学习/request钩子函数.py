from flask import Flask, request
import time

app = Flask(__name__)


@app.route('/hello')
def hello():
    time.sleep(2)
    print('hello')
    return 'hello'


@app.route('/view')
def view():
    print('view')
    return 'view'


@app.before_request
def before_request_one():
    print('before_request_one', request.url)
    # return 'before_request_one'


@app.before_request
def before_request_two():
    print('before_request_two')
    # return 'before_request_two'


# before_first_request 已被弃用，before_first_request 的作用是整个Flask应用在处理第一个请求时，运行的初始化代码
# 无论后续的请求是否是相同的请求，都不会再次运行。
# 同样的，如果该请求返回了响应体，flask 也会直接使用该响应体，并跳过后续的钩子和函数。
# 原则来说：根据 before_request 执行顺序的定义，想要实现 before_first_request 的效果，应该将函数放在第一个去定义 before_request
@app.before_request
def initialize():
    if 'INITIALIZE' not in app.config:
        app.config['INITIALIZE'] = True
        print('before_first_request_one')

        # return 'before_first_request_one => initialize'


@app.before_request
def initialize_two():
    if "INITIALIZE" not in app.config:
        print('before_first_request_two => ')
    else:
        print('已使用第一次请求')


@app.after_request
def after_request_one(response):
    print('after_request_one')
    return response


@app.after_request
def after_request_two(response):
    print('after_request_two')
    return response


# teardown_request 钩子函数在 after_request 函数之后执行，且同样是先绑定的后执行。
@app.teardown_request
def teardown_request_one(exc):
    print('teardown_request_one', exc)
    return 'teardown_request_one'


@app.teardown_request
def teardown_request_two(exc):
    print('teardown_request_two', exc)


if __name__ == '__main__':
    app.run(port=9099, debug=True)
