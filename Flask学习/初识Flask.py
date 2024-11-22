from flask import Flask

# 传入当前模板的文件名，有助于 Flask 确定根目录
app = Flask(__name__)


# 校验函数，始终为 false
def verify(func):
    def wrap(*args, **kwargs):
        if 'username' == 'gjh':
            res = func(*args, **kwargs)
        else:
            return '失败'

        return res

    return wrap


# app 为 flask 中的实例。
# 实例中的route方法，内部会将通过 add_url_rule 方法将传入的函数（view_func）和 端点（end_point）做映射。
# 如果没有指定 end_point 则默认为 view_func.__name__
# 在路由表中，通过 rule(router_path) 跟 end_point 做映射，在通过 end_point 找到对应的 view_func 来执行相应请求的功能。
# 注意：由于上方的找寻路由及路由对应的函数，所以要确保 end_point 的唯一性，尤其是当使用了 装饰器时，防止 end_point 为装饰器名称。
# 注意：在使用 route 时，需要确保 route 装饰器处于最上层，这样可以确保路由对应的函数功能不会缺失。route 只会对传入的函数绑定到路由表中进行映射
#     由于传入装饰器的函数并不是最顶层的函数，导致路由表绑定的是传入 route 的函数便终止了。
# 解析：假设在请求的地址对应为执行函数 =》 index 函数，在这之前进行效验（verify函数），校验出错便不会进行后续的执行函数（index）
# 解析：下方可以正常实现功能，假设verify 判断为错误，便不会执行index。
#   传入到 route 函数的是经过 verify 函数包装过后的函数，该函数包括了 verify 和 index的功能
@app.route('/')
@verify
def index():
    return 'Hello World'


# 示例：route路由不在首位：注意函数名不代表函数的真实地址，函数名可能更换，但函数地址为真实地址
# 理解：装饰器执行时从下至上进行包装，所以传入 route 装饰器的函数是 hello 函数对应的函数地址。
# 然后将 route 装饰器返回的函数传给 verify 进行包装，最后将 verify 返回的函数地址重新复制给 hello
# 注意；上述，最后 hello 的函数对应的函数地址已经不是初识的 hello 函数地址空间了。
#   但是在传入 route 时，route 内部操作的是初始的 hello 函数地址空间，导致在路由表中，/hello 地址对应的执行函数，便是最初的 hello 函数地址空间。
#   导致 verify 函数不会进行执行。
# 总结：之所以 route 要在最外层，就是确保最终的装饰器返回的函数，可以被映射到路由表中。可以被 route_path 匹配并执行。
@verify
@app.route('/hello')
def hello():
    return 'Hello World'


if __name__ == '__main__':
    # host 表示哪些主机可以访问本地服务器，port 表示端口，debug 表示调试
    app.run(host='0.0.0.0', port=5001, debug=True)
