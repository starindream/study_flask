from sqlalchemy import create_engine, String, Table, MetaData, Column, Integer, insert, select, ForeignKey, bindparam
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from typing import Optional

"""
    总结：
        1、insert 语句只能作用在 Table 直接生成的对象使用，如果想要作用在声明式对象，则需要直接传入整个声明式类，在:Select中举例。
        2、insert 语句相当于是将当前的表对象生成一个 INSERT INTO 的 SQL 语句，如果没有使用后续的 values 方法
            则生成的 sql 语句中，会对所有的列进行新增，传递了 values 参数，则只会对 values 中的列进行新增。
        3、使用 insert(user_table) 虽然会直接生成一个 SQL 语句，且语句中会包含所有列的名称，但是由于传递参数是根据键值对的形式传参的
            所以最终在内部处理时，会将列的名称跟参数一一对应，当出现列名存在，但参数不存在时，会取消SQL中的该列名，改为不对该列新增。
        4、注意：values 中参数会和最终的 execute 中的参数进行整合，一起传递到数据库。
        5、where 语句中传递的参数不会直接计算，python会判断当前的计算，如果时 SQLAlchemy 的计算，则不会直接返回结果，而是生成一个表达式对象
            在内部保存，在最后execute时，才会转化为 SQL 语句传递到数据库。
            原因：SQLAlchemy 重载了 python 中的 运算符，导致在运算符时，会判断是否是 SQLAlchemy对象，是的话则会转化成 SQL 表达式对象。
        6、scalar_subquery 相当于会直接返回单行单列的具体的值，使用了 scalar_subquery 返回的则会是一个具体的值，而不会是一个SQL表达式对象。
"""

engine = create_engine("mysql+pymysql://root:a123456789@localhost/demo")

metadata = MetaData()

# class Base(DeclarativeBase):
#     pass


# class User(Base):
#     __tablename__ = 'user_account'
#
#     # 主键
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     # 名称
#     name: Mapped[str] = mapped_column(String(30))
#     # 全名
#     fullname: Mapped[Optional[str]] = mapped_column(String(50))


user_table = Table('user_account', metadata, Column('id', Integer, primary_key=True),
                   Column('name', String(30), nullable=False),
                   Column('fullname', String(30)))

address_table = Table('address', metadata, Column('id', Integer, primary_key=True),
                      Column('user_id', ForeignKey('user_account.id'), nullable=False),
                      Column('email_address', String(200), nullable=False))


# class Address(Base):
#     __tablename__ = 'address'
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


def declara_insert_user():
    # 使用声明式对象来触发 insert 方法。
    address = Address()
    result = insert(address)
    print(result)


def insert_user():
    # 使用声明式对象来触发insert语句。
    # address = Address()
    # address.insert()

    # 使用 Table 对象来触发insert
    # stmt = user_table.insert()

    stmt = user_table.insert().values({'name': 'test4'})

    print(stmt)
    compiled = stmt.compile()
    print(compiled.params)

    # with engine.begin() as con:
    #     con.execute(stmt)

    # with engine.connect() as con:
    #     con.execute(stmt, {'name': 'test2'})
    #     con.commit()

    with engine.connect() as con:
        con.execute(stmt, {'fullname': 'fullname2'})
        con.commit()


# ----------------------练习-----------------------

def insert_user_table():
    stmt = insert(user_table).values(name='Tom', fullname='ChenTom')
    with engine.connect() as con:
        con.execute(stmt)
        con.commit()


def insert_address_table():
    print('insert', user_table.insert().values())
    print('params', user_table.c.name == 'Tom')
    # 使用了 scalar_subquery() 返回的则是一个具体的值，而不是一个SQL语句的表达式对象
    sub_query = select(user_table.c.id).where(user_table.c.name == bindparam('username')).scalar_subquery()
    stmt = insert(address_table).values(user_id=sub_query)
    print('stmt', stmt)

    with engine.connect() as con:
        # 不能执行 scalar_subquery() 的返回信息
        # result = con.execute(sub_query, {'username': 'Tom'})

        # sql = user_table.select().where(user_table.c.name == bindparam('username'))
        # result = con.execute(sql, {'username': 'Tom'})
        # for i in result.fetchall():
        #     print(i)

        con.execute(stmt, {'email_address': '2624276700@qq.com', 'username': 'Tom'})
        con.commit()


if __name__ == "__main__":
    # Base.metadata.drop_all(engine)
    # metadata.drop_all(engine)
    metadata.create_all(engine)
    # insert_user()
    # declara_insert_user()
    # insert_user_table()
    insert_address_table()
    pass
