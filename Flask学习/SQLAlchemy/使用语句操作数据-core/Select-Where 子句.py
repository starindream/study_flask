from sqlalchemy import create_engine, select, String, ForeignKey, insert, and_, or_
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional

"""
    总结：
        1、where 子句中的当使用SQLAlchemy中的类进行了运算符判断，返回的会是一个 SQL 表达式对象，而不是一个 布尔值。
        2、where子句可以放入多个条件，多个条件之间是并列（and）的关系
        3、在where子句中，如果想表示 and 和 or 的用法，可以使用方法 and_ 和 or_，使用 IN 子句，则需要使用 User.name._in(List)
        4、filter_by 子句常用来表示简单的相等的语句，如 filter_by(a=1,b=1) 转化为sql则为 WHERE a=1 AND b=1
        5、在 SQL 中 || 表示字符串连接符。
"""

engine = create_engine("mysql+pymysql://root:a123456789@localhost/demo")


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    fullname: Mapped[Optional[str]] = mapped_column(String(50))


class Address(Base):
    __tablename__ = 'address'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id = mapped_column(ForeignKey('user_account.id'), nullable=False)
    email_address: Mapped[str] = mapped_column(String(50), nullable=False)


def insert_user():
    stmt = insert(User)
    with engine.connect() as con:
        con.execute(stmt, [{'name': 'Lisi', 'fullname': 'ChenLisi'}, {'name': 'Hua', 'fullname': 'ChenHua'}])
        con.commit()


def select_where():
    # stmt = select(User).where(User.name == 'Lisi', User.fullname == 'ChenLisi')
    stmt = select(User).where(User.name.in_(['Lisi']))
    with engine.connect() as con:
        result = con.execute(stmt)
        print('result', result.mappings())
        for item in result.mappings():
            print(item)
    print('where => stmt', stmt)


def select_where_and():
    stmt = select(User).where(and_(User.name == 'Lisi', User.fullname == 'ChenLisi'))
    print(stmt)
    with engine.connect() as con:
        result = con.execute(stmt)
        for i in result.mappings():
            print(i)


def select_where_or():
    stmt = select(User).where(or_(and_(User.name == 'Lisi', User.fullname == 'ChenLisi'), User.name == 'Tom'))
    print('stmt')
    with engine.connect() as con:
        result = con.execute(stmt)
        for item in result.mappings():
            print(item)


def select_like_start_with():
    stmt = select(User).where(User.name.startswith('L'))  # SELECT * FROM user_account WHERE name LIKE 'L' || '%'
    print(stmt.compile())
    print('stmt', stmt)
    with engine.connect() as con:
        result = con.execute(stmt)
        for item in result.mappings():
            print(item)


def select_like():
    stmt = select(User).where(User.name.like("L%"))
    print(stmt)
    with engine.connect() as con:
        result = con.execute(stmt)
        for item in result.mappings():
            print(item)


def select_filter_by():
    # 由于filter_by 是通过传递参数赋值来进行判断的，所以可以直接传递类的属性等于某个值的形式，内部会做相应的处理
    # 内部 filter_by 会生成相应的参数等于参数值的 SQL 语句，多个参数之间形成 AND 并列的条件
    stmt = select(User.name.label('Username'), User).filter_by(name='Lisi', fullname='ChenLisi')
    print(stmt)
    with engine.connect() as con:
        result = con.execute(stmt)
        for item in result.mappings():
            print(item)


def select_add():
    stmt = select(User).where(User.id + '1' == 2)
    print('stmt', stmt)
    with engine.connect() as con:
        result = con.execute(stmt)
        for item in result.mappings():
            print(item)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    # insert_user()
    # select_where()
    # select_where_and()
    # select_where_or()
    # select_filter_by()
    # select_like_start_with()
    # select_add()
    # select_like()
    print(and_(User.name == 'test'))
