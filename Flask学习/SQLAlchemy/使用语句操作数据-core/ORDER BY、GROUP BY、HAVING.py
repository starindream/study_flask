from sqlalchemy import create_engine, String, select, ForeignKey, alias
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional, List

engine = create_engine("mysql+pymysql://root:a123456789@localhost/demo")

"""
    知识点：
    1、ORDER_BY、GROUP_BY
    2、label、alias
"""


class Base(DeclarativeBase):
    pass


class Emp(Base):
    __tablename__ = "t_emp"

    empno: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    ename: Mapped[Optional[str]] = mapped_column(String(20))
    job: Mapped[Optional[str]] = mapped_column(String(20))
    deptno: Mapped[Optional[int]] = mapped_column(ForeignKey("t_dept.deptno"))
    # dept: Mapped["Dept"] = relationship("Dept", back_populates='emps')


class Dept(Base):
    __tablename__ = 't_dept'

    deptno: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    dname: Mapped[Optional[str]] = mapped_column(String(20))
    loc: Mapped[Optional[str]] = mapped_column(String(20))
    # emps: Mapped[List["Emp"]] = relationship(Emp, back_populates='dept')


def select_order_by():
    # stmt = select(Emp,Dept).join(Emp, Emp.deptno == Dept.deptno)
    stmt = select(Emp, Dept).join_from(Emp, Dept, Emp.deptno == Dept.deptno).order_by(Emp.deptno.desc())
    print(stmt)
    print('desc', Emp.deptno.desc())


def select_group_by():
    # stmt = select(Emp.deptno.label("new_deptno")).group_by(Emp.deptno)
    # 注意：别名可以作用于 group_by 和 order_by 语句中
    stmt = select(Emp.deptno.label('new_deptno')).group_by("new_deptno")
    print(stmt)

    with engine.connect() as con:
        result = con.execute(stmt)
        for item in result:
            print('result', item)


def select_alias():
    # alias 通常用来设置表的别名，label通常用来设置列的列名
    new_emp = alias(Emp)
    stmt = select(new_emp)
    print(stmt)
    with engine.connect() as con:
        result = con.execute(stmt)
        for item in result:
            print(item)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # select_order_by()
    # select_group_by()
    select_alias()
