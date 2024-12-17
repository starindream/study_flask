from sqlalchemy import create_engine, String, select, ForeignKey, func, literal_column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional, List

"""
    总结：
        1、显示调用 FORM 方法有，select_form、join_form、join，前者可以确定从哪个表回去信息，后两者必须要进行表连接，则需要两张以上的表进行查询。
            区别：select_form 可以使用在一张表的显示Form 上，而 join_form 和 join 都必须要使用两张表以上的显示FORM。
            join_form 和 join 的区别，join 是进行内连接，且内部参数只支持传入一张表，且能使用 ON 条件和和表外连接。
            join_form 则可以传入两张表进行表连接。
            建议多使用 join
        2、要显示的调用 FORM 进行表连接需要 join_form 方法，ON 子句在 join_form 方法的后方参数可以添加相应的类似于 where中的 sql 表达式的判断条件。
        3、当 select 和 join_form 中有不同的表，则 select 和 join_form 中的表，都会出现在 FORM 子句中，但只有 join_form 中的表连接会存在 ON 条件。
        4、要使用 表外连接，需要在 join_from 中传递参数 isouter=True ,连接便会成为 左连接 
"""

engine = create_engine("mysql+pymysql://root:a123456789@localhost/demo")


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user_account'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]] = mapped_column(String(30))


class Emp(Base):
    __tablename__ = "t_emp"

    empno: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    ename: Mapped[Optional[str]] = mapped_column(String(20))
    job: Mapped[Optional[str]] = mapped_column(String(20))
    deptno: Mapped[Optional[int]] = mapped_column()
    dept: Mapped["Dept"] = relationship("Dept", back_populates='emps')


class Dept(Base):
    __tablename__ = 't_dept'

    deptno: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    dname: Mapped[Optional[str]] = mapped_column(String(20))
    loc: Mapped[Optional[str]] = mapped_column(String(20))
    emps: Mapped[List["Emp"]] = relationship(Emp, back_populates='dept')


def select_not_have_table():
    stmt = select(User.id)
    print(stmt)
    with engine.connect() as con:
        result = con.execute(stmt)
        for item in result.mappings():
            print(item)


def select_join_form():
    # 注意如果使用了 Select 和 join_from ，Select 和 join_from 中的表都会进行表连接
    # 但是只有 join_from 中的子句会进行 ON 子句连接
    stmt = select(User).join_from(Emp, Dept, Emp.deptno == Dept.deptno, isouter=True)
    print(stmt)


def select_join():
    # 不可使用，因为select中没有表，join进行的是表连接，但是整个SQL语句只有一张表
    # stmt = select(literal_column("COUNT(*)")).join(User)
    # stmt = select(literal_column("COUNT(*)")).join(Dept, Emp, Dept.deptno == Emp.deptno)
    stmt = select(literal_column("COUNT(*)")).select_from(Emp).join(Dept, Emp.deptno == Dept.deptno, isouter=True)

    print(stmt)


def select_join_form_and_join():
    # 表连接可以进行多次连接，却内部的列名都可以识别出当前列位于哪张表中，最后的连接，可以通过前面连接的表的列名继续进行判断
    stmt = select(literal_column("'custom")).join_from(Emp, Dept, Emp.deptno == Dept.deptno, isouter=True).join(User,
                                                                                                                User.id == Dept.deptno)
    print(stmt)


def select_test():
    # 不可以在where中使用 label，因为 label 返回的东西跟原本的类对象中的属性name有所不同，不能进行运算符重载为SQL表达式对象。
    # stmt = select(User).where(User.name.label('username') == 'Lisi')
    pass


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # select_not_have_table()
    # select_join_form()
    select_join()
    # select_join_form_and_join()
