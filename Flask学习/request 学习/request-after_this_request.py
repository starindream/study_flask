from flask import Flask, after_this_request, jsonify

app = Flask(__name__)


@app.before_request
def before_request():
    print('before_request')

    # 当使用了 before_request 和 after_this_request
    # 执行顺序：before_request => route => after_this_request
    @after_this_request
    def after_request(response):
        print('after_requst', response)
        return jsonify('after_request')


@app.route('/view')
def view():
    print('view')
    return jsonify('view')


@app.route('/test')
def test():
    print('test')
    return jsonify('test')


if __name__ == "__main__":
    app.run(port=10001)
