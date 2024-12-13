from sqlalchemy import create_engine, update, select, String, ForeignKey, bindparam, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional

"""
    总结：
        1、注意：SQLAlchemy 中的 update 语句 不可以一次性更新多张表，即不能在 update 中进行表连接
        2、如果要更新多张表，在values中采用 values({table1.name:value,table2.name:value})的形式更改，两张表的连接条件，使用 where子句连接。
        3、更新多个值 values(name1=value1,name2=value2)
        4、delete 只能删除一张表，即使进行了表连接，也只会删除 delete(table1).where(table1.id=table2.id) delete 中传递的 table1 表。
"""

engine = create_engine("mysql+pymysql://root:a123456789@localhost/demo")


class Base(DeclarativeBase):
    pass


class Emp(Base):
    __tablename__ = 't_emp'

    empno: Mapped[int] = mapped_column(primary_key=True)
    ename: Mapped[Optional] = mapped_column(String(20))
    deptno: Mapped[Optional[int]] = mapped_column(ForeignKey("Dept.deptno"))


class Dept(Base):
    __tablename__ = 't_dept'

    deptno: Mapped[int] = mapped_column(primary_key=True)
    loc: Mapped[Optional[str]] = mapped_column(String(20))
    dname: Mapped[Optional[str]] = mapped_column(String(20))


def update_stmt():
    stmt = update(Emp).values(ename='TEST').filter_by(empno=9000)
    print(stmt)

    print(stmt.compile().params)

    with engine.connect() as con:
        result = con.execute(stmt)
        # for item in result:
        #     print(item)
        con.commit()


def update_many():
    many_stmt = update(Emp).values(ename=Emp.ename + bindparam("name")).filter_by(empno=bindparam("b_empno"))
    print(many_stmt)
    with engine.connect() as con:
        con.execute(many_stmt, [{"name": '9000', "b_empno": 9000}, {"name": '8000', "b_empno": 8000}])
        con.commit()


def update_more_values():
    stmt = update(Emp).values(ename='value', deptno=90).filter_by(empno=9000)
    print(stmt)

    with engine.connect() as con:
        con.execute(stmt)
        con.commit()


def update_sort_values():
    # 有序传递多个参数
    stmt = update(Emp).ordered_values((Emp.ename, 11), (Emp.deptno, Emp.ename + 11)).where(Emp.empno == 9000)
    print(stmt)
    print(stmt.compile().params)
    with engine.connect() as con:
        con.execute(stmt)
        con.commit()


def relation_update():
    subq = select(Dept.dname).where(Emp.deptno == Dept.deptno).scalar_subquery()
    subq2 = select(Dept.deptno).where(Emp.deptno == Dept.deptno).scalar_subquery()

    # 该方法在 MySQL 中不支持，但是可以通过python实现，可能是 python 在中间进行了处理，pg 数据库可以实现 下方updateq 返回的 SQL 语句。
    pref = select(Dept.dname, Dept.deptno).where(Emp.deptno == Dept.deptno).subquery()

    updateq = update(Emp).filter_by(deptno=pref.c.deptno).values(ename=pref.c.dname)

    print(updateq)

    with engine.connect() as con:
        con.execute(updateq)
        con.commit()


def update_more_tables():
    stmt = update(Emp).where(Dept.deptno == Emp.deptno).where(Emp.empno == 9000).values({
        Emp.ename: 'TESTMORE',
        Dept.dname: 'DEPTEMPRE'
    })

    with engine.connect() as con:
        con.execute(stmt)
        con.commit()


def delete_stmt():
    stmt = delete(Dept).where(Emp.deptno == Dept.deptno).where(Emp.empno == 9000)
    print(stmt)
    with engine.connect() as con:
        result = con.execute(stmt)
        # for item in result:
        #     print(item)
        con.commit()


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    # update_stmt()
    # update_many()
    # relation_update()
    # update_more_tables()
    # update_more_values()
    # update_sort_values()
    delete_stmt()
