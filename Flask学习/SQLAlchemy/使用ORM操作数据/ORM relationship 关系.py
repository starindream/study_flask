from sqlalchemy import create_engine, String, ForeignKey, Column, Table
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column, sessionmaker
from typing import Optional, List

engine = create_engine("mysql+pymysql://root:a123456789@localhost/demo")

session_factory = sessionmaker(engine)

"""
    总结：
        1、relationship 的作用是可以让 SQLAlchemy 可以知道两个类之间的关系，可以自动进行关联，而不需要手动去进行关联
        2、外键的定义是需要的，主要可以让 SQLAlchemy 知道两张表的通过什么来进行关联的，一般确认关联关系，可以通过 ForeginKey 和 primaryjoin
            注意：主要还是建议使用 ForeginKey ，因为可以自动维护表的关系，如当父表删除，可以自动删除子表的内容。
        3、backref 和 back_populate 都是相同的作用，定义多张表之间的反向关系.
            可以理解为 relationship 定义的属性，就是用来存储内部关联的类的实例对象。
            backref 和 back_populate 则是可以让我们从一个模型中访问另一个模型的实例。
            理解：
            relationship 定义的属性便是用来存储对应关系类的实例，而back_populate 定义的值，则是对应关系类中，关联当前类的属性
            back_populate 需要两个相应关系的类中都手动定义 relationship，来确认当前用于存储其他对象类的实例属性,并通过这两个属性来进行同步
            backref:只需在一个类中定义 relationship 即可，对应的关联类，会自动创建一个 relationship 并生成一个属性，反向关联到当前类。
            back_populete：表示连接两个类中的属性，并进行同步
            假设：只有 Author 定义了 relaionship ，则变为了单向关系，只能通过 Author 找到 Books 的数据，无法通过 Books 找到 Author的数据
                而定义 back_populate 则可以保证两个关系可以同步，保证数据一致，当添加Author中的Books实例，可以自动在 Books 中的对应属性，添加 Author的对应关系。
            
            自理解
            1、back_populate作用就是当前类存储关联类的实例对象时，可以通过设置的back_populate 属性，可以找到关联类存储当前类实例的属性，然后将当前实例存储到关联类对应的属性中，实现同步。
                总结：backpopulate让父类添加子类实例时，可以反向让子类添加当前父类实例，实现同步
            2、向类中的 relationship 属性添加实例时，会默认通过back_populate方向向关联类中的对应relationship添加当前的类的实例。
           
            back_populate:
            
            Author:
            books = relationship("Book",back_populate="author") # back_populate 表示反向关系，对应类关联到本类的关系
            
            Book:
            author = relationship("Author",back_populate="books")
            
            backref:
            
            Author：
            books = relationship("Book",backref="author")
        4、uselist 可以设置为当前的存放其他类实例的属性是否为一个集合，当为一个集合时，可以存储多个其他类实例，实现多对一的操作，
            当设置为false，只能存储一个他类的实例，当重复进行添加时，会将上一个覆盖，相当于实现 一对一或一对多的关系。
        5、foreignKey 同样可以定义关系，相当于定义了当前类存储关联类的实例对象，但不能让关联类存储当前类的实例对象。
"""


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20))

    books = relationship("Book", back_populates="author", uselist=False)


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(20))
    # 如果不使用 ForeignKey，也需要定义 author_id ，否则无法定义出 Author 和 Book 之间的关系
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'))

    author = relationship("Author", back_populates="books")


def insert_books():
    session = session_factory()

    # 将 book1 和 book2 添加至 tom 的 books 中，当进行add 时，会自动将books中的书籍进行添加，并跟当前的 author 进行绑定关联。
    # back_populates 可以理解为该类中的列去存储子类生成的实例对象。使我们可以从一个模型中访问另一个模型。
    # 如：下方可以通过 将定义的author属性传入为 tom，则会自动将 tom中的books关联上book1 和 book2，这样在添加 tom 时，会自动添加 book1和book2
    tom = Author(name='tom')
    book1 = Book(title='book1', author=tom)
    book2 = Book(title="book2", author=tom)

    # 多对多情况下，books 中会存在两个对象。
    print(tom.books)

    # 当在 一对一情况下， 设置了 books uselist false 则books中只会存在最新的数据 book2，不再为一个列表
    print(tom.books.__dict__)

    session.add(tom)
    session.commit()

    session.close()


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)
    # insert_books()
