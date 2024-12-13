from sqlalchemy import insert, String, select, create_engine, bindparam, ForeignKey, text, literal_column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import List, Optional

"""
    总结：
        1、使用 insert、select 等方法操作声明式对象时，是直接操作声明式类，而不是实例对象，操作Table类的衍生，才是实例对象。
        2、声明式类在使用时，直接操作整个类，则表示整个表结构，如果时类中的某个属性，则是相当于是表结构的某个字段。
        3、select(table1,table2) 这种结构相当于是将 table1 和 table2 进行表连接。
        4、想要传递常量，则需要使用 text 方法来定义数据，转化为常量传入 select 语句中。
            指定需要定义将常量进行两次字符转义，一次是使用在text中，一次是传入到mysql中。
            在text中， 会将其变绎成SQL表达式，会去除字符串引号，所以需要加两层，如：text("'custom'")
            官方回答：请注意，当使用 text 和 literal_column 时，正在编写的其实是 SQL 表达式，不会对传入的数据进行转义，而是直接添加值SQL表达式中。
                所以需要在添加到SQL表达式上时，还需要使用引号包裹，防止被当作变量使用，不是文字值，因此，我们必须包含要呈现的SQL所需的任何引号和语法。
        5、对于常用的 表达式 (如：列名，函数：NOW()，复杂条件:age>8 ) 的 SQL 可以使用 literal_column，且 literal_column 可以添加label做别名
            注意，literal_column 不会对传入的数据进行转义，而是直接添加到SQL表达式上，需要注意防止发生 SQL 注入。
          5.1 text 和 literal_column 都是直接将内部的语句原样添加至SQL语句中，不会进行转义处理。
        6、如果想要为查询出的表中的列设置别名，则需要使用 label 方法。
            label 中定义的字符串，便是返回的表结构对应列的别名，如：User.name.label('username')，Column定义的对象，可以使用 label 方法。
        7、自定义返回的表列的结果，如：select(('Username：'+User.name).label('username))
            像上述中定义的返回列，会对每行返回的数据都会加上前缀 Username：并且定义表头的列名为 username
        
        
"""

# 创建数据库连接，让python中的表对象可以找到数据库
engine = create_engine("mysql+pymysql://root:a123456789@localhost/demo")


# 创建基类
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]] = mapped_column(String(50))


class Address(Base):
    __tablename__ = 'address'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey('user_account.id'), nullable=False)
    email_address = mapped_column(String(50), nullable=False)


# 使用声明式类使用 select
def declara_select():
    # ins_stmt = insert(User).values(name="Tom", fullname="ChenTom")
    # with engine.connect() as con:
    #     con.execute(ins_stmt)
    #     con.commit()

    subquery = select(User.id).where(User.name == bindparam('username')).scalar_subquery()
    insert_stmt = insert(Address).values(user_id=subquery)
    with engine.connect() as con:
        con.execute(insert_stmt, {'email_address': "2624276700@qq.com", "username": "Tom"})
        con.commit()

    stmt = select(User).where(User.name == 'Tom')
    # result = stmt.compile()
    # print(result.params)
    # stmt = insert(User)
    print(stmt)
    with engine.connect() as con:
        result = con.execute(stmt)
        print('first', result.first())
        # for i in result.fetchall():
        #     print('结果', i)


# 使用声明式对象，查询出用户的姓名及对应的地址信息
# 使用表连接
def declara_join_table():
    stmt = select(User.name, Address).where(User.id == Address.user_id).order_by(Address.user_id)
    print('declara_stmt', stmt)
    with engine.connect() as con:
        result = con.execute(stmt).all()
        print('join 结果', result)


# 使用 text 方法来传递常量，及使用label来定义别名
def declara_label():
    stmt = select(('Username：' + User.name).label('username'), text("'custom'"))
    print(stmt)
    with engine.connect() as con:
        result = con.execute(stmt)
        for i in result.mappings():
            print('label', i)


def declara_literal_column():
    # 不可使用
    # stmt = literal_column('SELECT * FROM t_emp')

    # stmt = text("SELECT * FROM t_emp")

    stmt = select(User, literal_column("SUM(user_account.id)"))

    print('declara_literal_column stmt', stmt)

    with engine.connect() as con:
        result = con.execute(stmt)
        print(result)


if __name__ == "__main__":
    # Base.metadata.drop_all(engine)

    Base.metadata.create_all(engine)

    # declara_select()
    # declara_join_table()
    # declara_label()
    declara_literal_column()
    pass
