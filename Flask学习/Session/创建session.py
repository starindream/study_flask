from flask import Flask, session, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ABCD'


@app.route('/hello')
def hello():
    session.update({
        'username': 'hello',
        'nihao': 'nihao ',
        'info': 'insorewqreqwreqwrqewrsadfadsfdsafadsfsfsd1',
        'wohao': 'wohao'
    })
    return jsonify({'message': 'hello'})


@app.route('/test')
def test():
    res = session.get('username')
    res1 = session.get('nihao')
    res2 = session.get('info')
    print('res', res, res1, res2)
    return jsonify({'message': res})


if __name__ == '__main__':
    app.run(port=9000, debug=True)
