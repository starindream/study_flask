from sqlalchemy import create_engine, union, select, String, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional

"""
    总结：
        1、UNION 可以使用 union 来进行连接两个查询，同样也会生成一个由 UNION 连接的 SQL 语句表达式
        2、union 方法同样可以使用 subquery 的属性方法，将生成的 union 变为子查询对象。用于 join连接操作
        3、同样可以使用 aliased 将 ORM类 映射到 union 形成的 subquery 子查询上。
        4、exists 可以判断当前查询是否具有记录，返回一个 boolean 值，TRUE/FALSE，常用作 where 表达式中。
        5、NOT EXISTS 则是在前面加上一个 ~ 否定符，~exists_stmt
        6、func 中包含了 大部分 SQL 中的函数，可以通过func.函数名的形式获取，最终会返回 SQL 函数表达式对象。
        7、窗口函数一般都是通过 func 函数的返回值再次调用 over 来实现，func.sun().over 通过函数名后续的 over 函数来使用，over函数内部的参数则表示确定窗口的范围。
"""

engine = create_engine("mysql+pymysql://root:a123456789@localhost/demo")


# DeclarativeBase 内部会自动生成 Table 对象，且内部自动管理一个 metadata 集合数据
class Base(DeclarativeBase):
    pass


class Emp(Base):
    __tablename__ = 't_emp'

    empno: Mapped[int] = mapped_column(primary_key=True)
    ename: Mapped[Optional[str]] = mapped_column(String(30))
    deptno: Mapped[Optional[int]] = mapped_column(ForeignKey('t_dept.deptno'))


class Dept(Base):
    __tablename__ = 't_dept'

    deptno: Mapped[int] = mapped_column(primary_key=True)
    loc: Mapped[Optional[str]] = mapped_column(String(20))
    dname: Mapped[Optional[str]] = mapped_column(String(20))


def union_select():
    one_stmt = select(Emp).where(Emp.deptno == 10)
    two_stmt = select(Emp).where(Emp.deptno == 30)
    u_stmt = union(one_stmt, two_stmt).subquery()
    print(u_stmt)
    stmt = select(Dept).join(u_stmt, Dept.deptno == u_stmt.c.deptno)
    print('stmt=>', stmt)

    with engine.connect() as con:
        result = con.execute(stmt)
        for item in result:
            print(item)


def exists():
    e_stmt = select(Dept.deptno).where(Dept.deptno == 100).exists()
    # NOT EXISTS 则是在前面加一个反选符 ~e_stmt
    print(e_stmt)
    stmt = select(Emp).where(e_stmt)
    print('stmt', stmt)
    with engine.connect() as con:
        result = con.execute(stmt)
        for item in result:
            print(item)


# 窗口函数
def over_select():
    stmt = select(Emp, func.count().over(partition_by=Emp.deptno).label('窗口函数汇总'))
    print(stmt)
    with engine.connect() as con:
        result = con.execute(stmt)
        for item in result.mappings():
            print(item)


# 自定义 列 和 值 形成自定义的表值函数
def json_value():
    # MySQL 函数不支持 SQLite 的方法 =》 json_each
    onetwothree = func.json_each('["one", "two", "three"]').table_valued("value")
    stmt = select(onetwothree).where(onetwothree.c.value.in_(["two", "three"]))
    with engine.connect() as conn:
        result = conn.execute(stmt)
        result.all()


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    # union_select()
    # exists()
    # over_select()
    json_value()
