from flask import Flask

app = Flask(__name__)


def test():
    return 'test'


app.add_url_rule('/test', endpoint='test', view_func=test, methods=['POST'])

if __name__ == '__main__':
    app.run(port=9099, debug=True)
