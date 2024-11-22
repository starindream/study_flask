from flask import Blueprint, jsonify

print('__name__:', __name__)

admin = Blueprint('admin1', __name__, url_prefix='/admin')


@admin.route('/hello',endpoint='admin-hello')
def hello():
    data = {
        'message': 'module_one=>hello'
    }
    return jsonify(data)
