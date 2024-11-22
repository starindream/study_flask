from flask import Flask, jsonify
from blue_print_one.module_one import admin

app = Flask(__name__)


@app.route('/hello')
def hello():
    print('hello')
    data = {
        'message': 'success',
    }
    print('locals =>', locals())
    print('dir =>', dir())

    return jsonify(data)


# @app.route('/admin/hello')
# def test_hello():
#     data = {
#         'message': 'test=>hello=>success'
#     }
#     return jsonify(data)


app.register_blueprint(blueprint=admin)

print(app.url_map)
print(app.view_functions)

if __name__ == "__main__":
    app.run(port=9099, debug=True)
