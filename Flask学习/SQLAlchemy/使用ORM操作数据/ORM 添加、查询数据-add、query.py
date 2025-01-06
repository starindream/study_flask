from sqlalchemy import create_engine, String, ForeignKey, select, func
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
from typing import Optional

"""
    总结：
        1、类的实例可以理解为数据库中的表的一行记录
        2、session 对象可以传入一个ORM类的实例，在内部生成连接，并将实例中的数据根据调用的方法转化为 SQL 对象，来进行添加数据。
        3、当事务提交后，添加前通过 ORM 类生成的实例对象会被重置，内部的属性会被清空，并且 session 中保存挂起状态的集合也会删除对应的实例对象。
        4、当使用 session.query 时，只有 当结尾使用 all或者first 才会将前面生成的 SQL 表达式发送到数据库，并获取游标，在 增/删中，也可以通过 udpate/delete 发送到数据库
            query、filter、filter_by、order_by、group_by 等语句都是生成 SQL 表达式对象，而不会发送到数据库，当使用 all 时才会发送到数据库。
        5、session.query().all() 返回的是一个 集合 ，集合内会包含所有的返回数据
            返回的数据格式：
                1、如果定义返回的列使用 ORM类传入的，则该部分的所有列，会生成一个 实例对象返回
                2、如果定义的列不是整个 ORM类，即使为 OEM类 中的某个属性，返回的该列也会是一个具体的数据（键值数据），而不是一个实例对象
                如：session.query(Emp.name,Emp).all() 返回的数据：['SIMITH',<Emp.object>]，object 中包含了其他列中的所有数据，以对象的形式存储
        6、可以通过 session.get 来通过传入 ORM类和主键，zd来获取一个关于ORM类的实例对象，可以理解为 通过session 和 主键去数据库查找相应的数据，并返回后，处理成ORM类的实例对象形式。
"""

engine = create_engine("mysql+pymysql://root:a123456789@localhost/demo")


class Base(DeclarativeBase):
    pass


class Emp(Base):
    __tablename__ = 't_emp'

    empno: Mapped[int] = mapped_column(primary_key=True)
    ename: Mapped[Optional[str]] = mapped_column(String(20))
    deptno: Mapped[int] = mapped_column(ForeignKey('t_dept.deptno'))


class Dept(Base):
    __tablename__ = 't_dept'

    deptno: Mapped[int] = mapped_column(primary_key=True)
    dname: Mapped[Optional[str]] = mapped_column(String(20))
    loc: Mapped[Optional[str]] = mapped_column(String(20))


def orm_insert():
    """
    生成 insert 数据，并理解session的用法
    """
    # 生成一条行记录
    orm_data = Emp(empno=80291, ename='orm_inser_one', deptno=50)
    print(orm_data)

    # 生成一个 session 对象，用于操作 orm 类型的操作
    session = Session(engine)
    # session 的 add 相当于 将对象添加至 session 对象内部的集合中，处于挂起状态，尚未生成 SQL 语句
    session.add(orm_data)

    print(orm_data.__dict__)

    # 将挂起的状态生成 SQL 语句并发送到数据库，但是不会提交当前事务
    session.flush()

    print('提交前', orm_data.__dict__)

    session.commit()

    # 查看session中挂起状态的集合
    print(session.new)

    # 当成功提交后，实例对象中的属性会被清空重置。并且session中挂起状态的集合也会删除对应的实例对象。
    print('提交后', orm_data.__dict__)


def query_orm():
    """
    生成 query 查询语句，并熟悉 session 的用法
    """
    # 创建操作 ORM类型，及返回的结果也为 ORM 实例对象的 Session对象，内部也是通过 engine.connect 创建的连接实现的
    session = Session(bind=engine)
    # 简单的查询
    query_st = session.query(Emp)
    # 返回的是 SQL表达式
    print('type=>', type(query_st))
    print('query_st', query_st)
    result = query_st.all()
    # 使用all后，返回的是多个 Emp实例对象 构成的集合
    print(result)

    print('-----------------返回的列跟 ORM的列 不是完整相同的------------------')
    # 结论：只要返回的列名跟定义的 ORM 类不相同，则不会返回实例对象，而是具体的数据，返回的如果是一个 ORM 类，则该ORM类包含的列会生成一个实例对象。
    query_st = session.query(Emp.ename, Emp).filter(Emp.empno == 9000)
    print(query_st)
    result = query_st.all()
    print(result)
    for item in result:
        print(item)

    print('----------filter------------------')

    # 使用 filter 条件查询，相当于是 where
    query_st = session.query(Emp).filter(Emp.ename == 'LOSI')
    print(query_st)
    # 使用 all 方法，将生成的 SQL 对象发送至数据库，并返回 实例对象 生成的集合
    result = query_st.all()
    print(result)

    # st = select(Emp).filter(Emp.ename == 'LOSI')
    # print('st', st.compile())

    print('-------------------order_by-------------')
    # 生成 SQL 表达式对象
    query_st = session.query(Emp).order_by(Emp.empno.desc())
    print(query_st)
    # 将 SQL 表达式发送到数据库，并返回一个由返回的数据形成的实例对象的集合
    result = query_st.all()
    print(result)
    # for item in result:
    #     print(item.__dict__)

    print('------------------group_by-------------')
    # 生成一个 SQL 表达式对象
    query_st = session.query(Emp.deptno, func.count()).select_from(Emp).group_by(Emp.deptno)
    print(query_st)
    # 返回的不是一个实例对象的集合，而是一个具体的数据的集合，因为 group_by 返回的列跟定义的 ORM 对象的列不能达到完整的期望结果
    result = query_st.all()
    print(result)
    # for item in result:
    #     print(item)

    print('--------------join-offset-limit 分页-------------')
    query_st = session.query(Emp, Dept).join(Dept, Emp.deptno == Dept.deptno).filter(Emp.deptno == 10).offset(2).limit(
        5)
    print(query_st)
    result = query_st.all()
    print(result)
    # for tp in result:
    #     for item in tp:
    #         print(item.__dict__)
    for emp, dept in result:
        print('emp', emp.__dict__)
        print('dept', dept.__dict__)


def session_get_primary():
    """
    通过主键来查找对应ORM类中的实例对象
    """
    session = Session(bind=engine)
    # 相当于会发送SQL语句到数据库，查找对应的id，然后将返回的列依据 ORM 类生成一个对应的实例对象。
    get_obj = session.get(Emp, 9000)
    print(get_obj)
    print(get_obj.__dict__)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # orm_insert()
    query_orm()
    # session_get_primary()
