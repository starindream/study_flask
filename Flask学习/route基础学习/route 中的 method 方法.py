from flask import Flask, url_for

app = Flask(__name__)


# methods 参数用于指定 url 允许的请求方式，可以为数组允许多个请求方式。
# 下方视图可以通过 get 和 post 两种请求方式来匹配到该视图。
@app.route('/hello', methods=['post', 'get'])
def hello():
    res = url_for('test')  # 打印出 /hello2 ，可以理解为 url_for 可以通过endpont 找到对应绑定的 url 路由地址，️而endpoint又可以找到函数地址
    print(res)
    return 'hello post'


@app.route('/hello2')
def test():
    return 'hello2'


if __name__ == '__main__':
    print(app.view_functions)
    print(app.url_map)
    app.run(port=5005)
