from flask import Flask

app = Flask(__name__)  # 生成flask实例，通过这个实例获取flask中的方法


def login(func):
    def wrap(*args, **kwargs):
        res = func(*args, **kwargs)
        return res

    return wrap


@app.route('/hello1')
@login
def hello():
    print('hello1')
    return 'hello1'


@app.route('/hello2')
@login
def hello2():
    print('hello2')
    return 'hell02'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
