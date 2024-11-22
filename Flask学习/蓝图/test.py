from flask import Flask, Blueprint

app = Flask(__name__)

# 定义蓝图
bp = Blueprint('test_blueprint_one', __name__)


@bp.route('/test')
def blueprint_route():
    return "This is the blueprint route"


# 注册蓝图
app.register_blueprint(bp)


# 主程序中的路由
@app.route('/test')
def main_route():
    return "This is the main app route"


bp_two = Blueprint('test_blueprint_two', __name__)


@bp_two.route('/hello')
def blueprint_route_two():
    return "This is the blueprint route two"


app.register_blueprint(bp_two)

if __name__ == '__main__':
    app.run(debug=True, port=10000)
