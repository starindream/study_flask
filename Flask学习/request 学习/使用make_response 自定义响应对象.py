from flask import Flask, make_response, jsonify, abort
import json

app = Flask(__name__)


@app.route('/hello')
def hello():
    print('hello')
    data = {
        'name': '张三',
        'age': 18
    }
    # response = make_response(json.dumps(data))  # make_response 的状态码定义的是 http 中的 status 状态码。
    # response.mimetype = 'image/png'
    # return response
    if data['name'] == '张三':
        print('abort')
        abort(500)

    return jsonify(data)


# errorhandler 可以处理相关的错误
@app.errorhandler(404)
def error_handle(err):
    print('处理错误', err)
    return jsonify('出现错误')


if __name__ == '__main__':
    app.run(port=9099, debug=True)
