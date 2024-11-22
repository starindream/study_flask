from flask import Flask, url_for
from werkzeug.routing import BaseConverter

"""
路由转换器：
作用：
1、路由转换器的作用就是当 路径 匹配成功后，需要进行转换的数据，是否满足定义数据时，需要的数据格式，如果满足，可以成功匹配视图并传递参数。
"""

# 创建 Flask 实例，通过实例启动方法
app = Flask(__name__)


class RegexConverter(BaseConverter):
    # 匹配规则
    # regex = 'g\d*'

    def __init__(self, url_map, regex):
        print('url_map:', url_map)
        self.regex = regex  # 通过路径re调用来确定匹配规则
        # super：获取当前传入的 self 的实例的 MRO 列表，并找到 RegexConverter 的下一个类，并调用该类中的方法，进行初始化。
        super(RegexConverter, self).__init__(url_map)

    def to_python(self, value):
        """这个函数主要是拿到了路由中的动态参数赋值给了 value，
        to_python 这个函数，可以操作动态参数
        返回操作之后的结果给匹配成功的视图函数作为形参。"""
        return value + '经python处理'

    def to_url(self, params):
        """
        通过 to_url 处理时，不会进行规则匹配
        这个函数用于和 url_for 连用，url_for通过指定给动态传参赋值给value
        我们可以根据 to_url 函数对传入的动态参数进行参数，然后将结果拼接在url上
        """
        return params + '经toUrl处理'


# url_map 在映射的过程中，flask 已经帮助我们定义了一部分转换器，当路由命中的数据满足转换器的要求后，便可以成功匹配视图。
app.url_map.converters['re'] = RegexConverter  # 定义新的规则转换


@app.route("/hello/<re('gjh.*'):value>")
def hello(value):
    print('value', value)
    # 通过 to_url 处理时，不会进行规则匹配，传递动态参数时，必须要使用 实参传递，指定参数名称，名称为路由动态参数的名称
    print('url_for：', url_for('hello', value='nihao'))
    return '参数：' + value


if __name__ == "__main__":
    app.run(debug=True, port=5003)
