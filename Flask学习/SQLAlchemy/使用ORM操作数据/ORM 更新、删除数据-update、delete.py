from sqlalchemy import create_engine, String, ForeignKey, select, insert
from sqlalchemy.orm import Mapped, DeclarativeBase, Session, mapped_column, declarative_base
from typing import Optional

"""
    总结：
        1、ORM类 使用更新操作，通过 session.query().filter().update({key:value}) 的形式来修改，会自动发送SQL语句，但不会提交事务。
        2、在使用 update 更新时，query中传入必须要是一个模型类或者表对象，如果传入单个列，返回的是单个列的结果集，而追踪不到整个表。
            可以理解的是，query、filter、update方法可以理解为都会保存对应的查询条件和数据，在最后的时候会进行整合并且输出。每一步都可以根据前面方法传入的条件或数据生成当前的SQL。
        3、query方法是一个灵活的查询构建器，默认的是生成 SELECT 语句，但后续如果具有update、delete，可以生成对应的 UPDATE、DELETE 语句
        4、session.delete 可以删除数据库返回的实例对象，不能删除自定义的实例对象，除非已被添加至数据库。
        5、session.query().filter().delete() 可以删除满足条件的数据
"""

# 创建数据库连接
engine = create_engine("mysql+pymysql://root:a123456789@localhost/demo")


class Base(DeclarativeBase):
    """
    继承子 DeclarativeBase 声明类，该类内部自动动在构造函数中，将子类的相关属性生成一个 Table 类
    """
    pass


class Emp(Base):
    """
    继承自Base类，根据类中定义的属性，自动生成一个 Table 类，用来描述数据库中表的字段。
    """

    __tablename__ = 't_emp'

    empno: Mapped[int] = mapped_column(primary_key=True)
    ename: Mapped[Optional[str]] = mapped_column(String(20))
    deptno: Mapped[Optional[int]] = mapped_column(ForeignKey('t_dept.deptno'))


class Dept(Base):
    __tablename__ = 't_dept'

    deptno: Mapped[int] = mapped_column(primary_key=True)
    dname: Mapped[Optional[str]] = mapped_column(String(20))
    loc: Mapped[Optional[str]] = mapped_column(String(20))


def update_execute():
    """
    结论：如果直接修改通过查询获取到的数据实例对象，会在下一次发送数据库时，自动进行修改
    :return:
    """
    session = Session(engine)

    emp = Emp(empno=9000, ename='9000-test', deptno=10)

    result = session.execute(select(Emp).where(Emp.empno == 9000)).fetchone()
    new_emp = result[0]
    print(result)
    for item in result:
        print(item.__dict__)

    print('session.new', session.dirty)

    new_emp.ename = '9000-test'
    print('session.dirty', session.dirty)
    result = session.execute(select(Emp).where(Emp.empno == 9000)).fetchone()
    item = result[0]
    print(item.__dict__)


def insert_execute():
    session = Session(bind=engine)
    session.execute(insert(Emp).values(empno=90998, ename='90998-test', deptno=10))
    session.commit()


def update_session():
    session = Session(engine)
    ut = session.query(Emp).filter_by(empno=9000)
    print(ut)
    session.query(Emp.ename, Emp.empno, Emp.deptno).filter_by(empno=9000).update({'ename': 'new1'})
    print(ut)
    session.commit()


def delete_session():
    session = Session(engine)
    # 下述不能通过 session.delete 删除，因为自定义的 del_emp 不是一个持久化对象，即不是一个数据库中的对象
    # 应该先从数据库查找返回实例对象，在通过 session.delete 删除
    dl_emp = Emp(empno=90998, ename='90998-test', deptno=10)
    db_emp = session.query(Emp).filter_by(empno=90998).first()
    # print(db_emp)
    session.delete(db_emp)
    session.commit()


def delete_query_session():
    session = Session(engine)
    session.query(Emp).filter_by(empno=80991).delete()
    session.commit()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    # update_execute()
    # insert_execute()
    # update_session()
    # delete_session()
    # delete_query_session()
