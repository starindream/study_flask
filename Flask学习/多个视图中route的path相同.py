from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'hello'


@app.route('/')
def hello2():
    return 'hello2'

app.run()