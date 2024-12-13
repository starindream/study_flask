from sqlalchemy import select, create_engine, String, ForeignKey, literal_column, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, aliased
from typing import Optional

"""
    总结：
    注意：所有的SQLAlchemy的方法都不是通过数据来进行整合的，而是将不同方法生成一个 SQL 表达式，最后将这些 SQL 表达式整合在一起，整个发送给 MySQL 才是真正开始执行的
        而不是某一部分先执行，获取数据再操作的步骤
        1、子查询需要使用 subquery方法来进行输出，否则在使用子查询进行连接操作时，会出现没有连接关系的错误。
        2、子查询需要使用 subquery 或者 alias 方法来为当前查询SQL中的表进行重命名，然后通过返回的新表对象中 c.column 属性来获取派生表的列名。
            理解：表连接时，使用子查询需要明确连接的目标，而正常的 select 返回的是一个 SQL 表达式对象，而通过 subquery 和 alias
                返回的 则是 一个表对象，join 可以针对该表对象进行连接等操作，同样也可以获取该表对象中的列等信息。
        3、Subquery 对象内部始终包含选择列的命名空间，Subquery.c 为查询列的命名空间。
        4、aliased 可以将 子查询 跟 ORM 类对象 进行关联，相当于将 传入的 subquery 当作 ORM类对象 的一个镜像，可以直接使用 ORM 操作。
            subquery返回的是表对象，操作列需要使用 Subquery.c.column
            aliased 返回的是一个子查询跟ORM类对象关联后的 ORM 模型对象，可以使用 ORM操作
                操作列使用 result=aliased(ORM,subquery) result.column
"""

engine = create_engine("mysql+pymysql://root:a123456789@localhost/demo")


class Base(DeclarativeBase):
    pass


class Emp(Base):
    __tablename__ = 't_emp'

    empno: Mapped[int] = mapped_column(primary_key=True)
    ename: Mapped[Optional[str]] = mapped_column(String(20))
    deptno: Mapped[int] = mapped_column(ForeignKey('t_deptno.deptno'))


class Dept(Base):
    __tablename__ = 't_dept'

    deptno: Mapped[int] = mapped_column(primary_key=True)
    dname: Mapped[str] = mapped_column(String(20))
    loc: Mapped[str] = mapped_column(String(20))


def subquery_select():
    sub_stmt = select(Dept).where(Dept.dname == 'RESEARCH').subquery('newDept')
    print('sub-stmt', sub_stmt)
    # stmt = select(Emp).join(sub_stmt, Emp.deptno == literal_column("'newDept.deptno'"))
    stmt = select(Emp).join(sub_stmt, Emp.deptno == sub_stmt.c.deptno)
    print('stmt', stmt)

    with engine.connect() as con:
        result = con.execute(stmt)
        for item in result:
            print(item)


def sub_select():
    substmt = select(Dept).where(Dept.dname == "RESEARCH").alias('new_dept')
    print(substmt)
    stmt = select(Emp).join(substmt, Emp.deptno == substmt.c.deptno)
    print(stmt)


def func_select():
    stmt = select(func.count(Emp.empno))
    print(stmt)


def aliased_subquery():
    sub_stmt = select(Dept).where(Dept.dname == 'RESEARCH').subquery('new_dept')
    print(sub_stmt)
    orm_stmt = aliased(Dept, sub_stmt)
    print(orm_stmt)
    stmt = select(Emp, sub_stmt).join(sub_stmt, Emp.deptno == orm_stmt.deptno)
    print(stmt)

    with engine.connect() as con:
        result = con.execute(stmt)
        for item in result:
            print(item)


def scalar_query():
    # 标量子查询，返回为单行单列的数据，通常同 聚合函数一起使用。
    scalar_stmt = select(Dept.deptno).where(Dept.deptno == 10).scalar_subquery()
    print(scalar_stmt)
    print(scalar_stmt == 10)

    stmt = select(Emp).where(Emp.deptno == scalar_stmt)
    with engine.connect() as con:
        result = con.execute(stmt)
        for item in result:
            print(item)


def relation_query():
    sub_stmt = select(Dept.dname).where(Dept.deptno == Emp.deptno).scalar_subquery()
    stmt = select(Emp, sub_stmt.label('new_dname'))
    print(stmt)

    with engine.connect() as con:
        result = con.execute(stmt)
        for item in result.mappings():
            print(item)


def test():
    substmt = select(Dept.deptno).where(Dept.deptno.in_([10, 20])).subquery()
    selectstmt = select(Dept.deptno).where(Dept.deptno.in_([10, 20]))
    print('substmt', substmt)
    print('selectstmt', selectstmt)
    print('-------------------------------')
    stmt = select(Emp).where(Emp.deptno.in_(substmt.c.deptno))
    # stmt = select(Emp).join(substmt, Emp.deptno == substmt.c.deptno)
    print(stmt)
    with engine.connect() as con:
        result = con.execute(stmt)
        for item in result:
            print(item)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    # subquery_select()
    # sub_select()
    # func_select()
    # aliased_subquery()
    # scalar_query()
    # relation_query()
    test()
    pass
