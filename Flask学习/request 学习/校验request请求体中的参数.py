from flask import Flask, request, make_response

app = Flask(__name__)


@app.route('/verify')
def verify_query():
    print('request', request.args)

    return make_response('hello word', 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=9008)
