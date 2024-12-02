from typing import List, Optional
from sqlalchemy import String, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

"""
    总结：
    1、声明类定义表，意思就是不是通过调用 Table 来定义表，而是通过声明一个类，在类中定义属性来定义表，类继承与 DeclarativeBase 基类，
        在基类中，内部会通过当前类的属性自动通过 Table 来定义一个表结构，并且基类中会维护一个 metadata 来存储所有继承与基类而定义的表结构。
    2、在声明表的类中，Mapped 是用来映射表中列的属性的,具体的约束还是得在 mapped_column 中定义
        mapped_column 是实际描述数据库中表的列信息的，同时可以描述出该列在数据库中的约束等。
    3、mapped_column 可以理解为将属性的值更改为一个字典，字典内部保存了该列名在数据库中的所有表结构信息。 

"""

# 创建数据库引擎
engine = create_engine("mysql+pymysql://root:a123456789@localhost/demo")


class Base(DeclarativeBase):
    pass


# 声明式定义表结构，可以通过 mapped_column 方法来将类中的属性定义为表中的结构，如果没有使用 mapped_column 定义的属性，则不会生成为表中的列
# 没有通过 mapped_column 定义的属性，就只是一个普通的类属性,如果没有约束，也可以通过 Mapped 来定义一个 ORM 映射属性。
class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]] = mapped_column(String(30))

    address: Mapped[List["Address"]] = relationship(back_populates='user')

    test = 1  # 没有通过 mapped_column 定义的属性

    test_map: Mapped[int]

    def __repr__(self):
        return f'User => id:{self.id},name:{self.name}'


class Address(Base):
    __tablename__ = 'address'

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(ForeignKey('user_account.id'))

    user: Mapped[List[User]] = relationship(back_populates='address')

    def __repr__(self):
        return f'Address=> id:{self.id},email_address:{self.email_address}'


if __name__ == "__main__":
    # sandy = User(name="sandy", fullname="Sandy Cheeks")
    # print(sandy)
    Base.metadata.create_all(engine)

    # Base.metadata.drop_all(engine)
