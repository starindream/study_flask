from sqlalchemy import create_engine, String, ForeignKey, Table, Column, Integer, or_, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker, backref
from typing import Optional

"""
    总结：
        关系口诀：一对多，多的表加外键。一对一，添加外键，并将外键设置为唯一性索引。多对多，三张表，中间表加外键，并且可以设置复合主键
        1、一对多关系，通常在多的一方会具有一个外键，来关联对应的唯一的表，而多对多的关系，则一般会使用一个中间表来映射两张表的主键关系。
        2、relationship 中 back_populate 确认哪两张表需要做关联，将具体的数据相互绑定，提交某一张表时，会自动操作另外一张表。
            secondary 则是确认将关联表在数据库中的关联关系映射在哪个中间表中，如保存两张表的主键关系。
        操作数据：
        1、在添加时，会将当前类模型中 relationship 属性中保存的关联类实例对象自动添加到数据库中。
        2、在查询时，也会在返回的实例对象中，查找到对应关系模型在数据库表中的数据并以实例对象的形式保存在当前实例对象中的 relationship 属性中。
        3、相当于不需要做两次操作，比如查找 author 为jack的作者以及对应的书籍
            那么只需要通过 session.query(Author).filter_by(name=jack)
            在返回的实例对象中的 relationship 属性中会自动保存 books 表中属于 jack 的书籍，相当于内部会自动根据relationship来做SQL操作，并将关联的数据保存在该属性中。
        4、在删除时，如果删除了 author 表的记录，则会自动删除 关联表中的数据，这是数据库 外键的特性。
        # cascade 参数未经代码证实。
        由于 author 和 book 没有外键关系，他们之间的关系通过关联表来映射，所以删除 author 并不能删除 book 的数据。
        数据库不能自动删除 book 的数据，可以通过配置，让 SQLAlchemy 来配置删除 book 的数据
        通过配置 relationship 中的 cascade 属性，可以让父表删除时，自动删除子表
        注意：只有配置了该属性的表删除时，会删除关联表的数据，如：a配置了属性，则a删除，会自动删除b相关数据，b删除，则不会删除a相关数据。
        5、在使用delete中可以传递参数 zq，该参数中的不同值，可以实现不同的效果，主要是让session中的 identity_map 跟数据库的数据同步时机。
        6、identity_map 是 session 内部维护 数据库中的数据与实例的一致性，确保数据库的一行记录只会存在一个实例。即使查询了多次数据库返回同一个实例对象，而不会创建新的实例对象。
            如果更改了 identity_map 中实例对象的属性，则在session.commit 时，会自动使用 UPDATE 进行更新。
            identity_map 中是通过主键来绑定实例对象的，所以当查询数据库返回的数据在identity_map中已经具有实例对象，则会直接返回，避免重复加载数据，创建实例对象。
            总结：identity 在 SQLAlchemy 中起到了至关重要的作用，保证了数据的一致性和避免了重复实例化，使得开发者可以高校且一致的管理数据库中的对象。
        7、identify_map 不会在查询时使用缓存，在每一次查询中，都会发送 SQL 语句到数据库中，然后通过数据库的返回数据看该数据的主键是否已经存在，存在的话，则会覆盖存在对象中的数据。
            注意：是覆盖数据，不会创建新的实例对象，可以理解为更改实例对象中的内容。
        8、只有经过了 session查询或者经过其他操作（如：使用 User类产生实例，并通过session.add(self)，来进行添加到数据库），才会生成一个实例对象放入 identity_map 中   
        9、session中的事务机制，在使用session触发数据库操作时（query、delete、add等），便会打开一个事务，一直到使用session.commit 或 session.flush 等操作才提交调该事务。
"""

engine = create_engine("mysql+pymysql://root:a123456789@localhost/demo")

session_factory = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


# 定义关联表、中间表、连接表
author_book = Table('author_book', Base.metadata,
                    Column('author_id', Integer, ForeignKey('authors.id', ondelete='CASCADE'), primary_key=True),
                    Column('book_id', Integer, ForeignKey('books.id', ondelete='CASCADE'), primary_key=True))


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    fullname: Mapped[Optional[str]] = mapped_column(String(20))

    # 定义用来存储 Book 实例对象的属性，通过 back_populate 来定义对应关联类，以及通过 back_populate 确认关联类中的 relationship 属性，实现同步。
    # secondary 确认中间表，back_populate 确认哪两张表需要做关联，secondary 确认将关联的数据映射在哪张中间表中。

    # books = relationship("Book", secondary=author_book, back_populates='authors')

    # 设置 cascade 让 SQLAlchemy 可以配置当 父表 删除时，自动删除子表的信息。由于没有外键，数据库无法找到对应的关系操作。
    # 问题：设置了 cascade 后，没有正常删除 Book 中的关联对象
    books = relationship("Book", secondary=author_book, back_populates='authors', cascade='all, delete')


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(20))

    authors = relationship("Author", secondary=author_book, back_populates='books', passive_deletes=True)


def add_book():
    jack = Author(name='jack')
    peter = Author(name='peter')

    book1 = Book(title='book1', authors=[jack, peter])
    book2 = Book(title='book2', authors=[jack, peter])

    # book1.authors.extend([jack, peter])
    # book2.authors.extend([jack, peter])

    # 可以从 jack 对象中获取提交的book
    for book in jack.books:
        print(book.__dict__)

    session = session_factory()

    session.add_all([book1, book2])

    session.commit()
    session.close()


def add_book_to_one():
    session = session_factory()

    tom = Author(name='tom')

    tom_book = Book(title='tom_book', authors=[tom])

    session.add(tom_book)
    session.commit()
    session.close()


def add_to_jack():
    session = session_factory()
    # 注意：下述方法错误，相当于重新添加了一个新的实例，这个实例也叫 jack，应该从数据库中获取到jack实例，而不是新创建一个jack实例
    # jack = Author(name='jack')
    # 正确做法：从数据库中获取jack，这样也会存在主键，而不是新创建的jack，新创建的不会存在主键，相当于是新创建一个jack，再进行关联。
    result = session.query(Author).filter_by(name='jack').first()
    print(result.__dict__)
    jack = result
    new_book = Book(title='new_book', authors=[jack])

    session.add(new_book)
    session.commit()
    session.close()


def search():
    session = session_factory()

    results = session.query(Author).filter_by(name='jack')

    for result in results:
        print(result.__dict__)
        print(result.books)
        for book in result.books:
            print('book', book.__dict__)

    # for book in jack.books:
    #     print(book.__dict__)

    session.close()


def delete():
    session = session_factory()
    session.query(Author).filter_by(name='jack').delete()
    session.commit()
    session.close()


def delete_one():
    session = session_factory()

    session.query(Author).filter_by(name='tom').delete()
    session.commit()
    session.close()


def delete_many_author_to_book():
    print('===================')
    # 解决：当删除 author 表中的一条数据时，删除book表中的只关联到jack表的数据，不删除关联了其他作者的数据
    # 思路：可以通过session获取到jack以及jack对应book的数据，在通过session查找jack内的book数据，判断哪些book中只关联了jack
    session = session_factory()

    results = session.query(Author).filter_by(name='jack').all()
    jack_books = []
    for result in results:
        print(result.__dict__)
        for book in result.books:
            print(book.__dict__)
            # 将 book 实例保存在数据中
            jack_books.append(book)

    print('=======处理 book 数据 =========')
    jack_book_name = [book.title for book in jack_books if 'title' in dir(book)]
    print(jack_book_name)
    books = session.query(Book).filter(Book.title.in_(jack_book_name)).all()
    jack_only_book = []
    for book in books:
        print(book.__dict__)
        # 原逻辑处理
        # for author in book.authors:
        #     print(author.__dict__)
        try:
            if len(book.authors) == 1 and book.authors[0].name == 'jack':
                jack_only_book.append(book)
        except Exception as e:
            print('Exception', e)
    print('======定义删除逻辑========')
    # print(or_(Author.name == 'jack', Book.id.in_([book.id for book in jack_only_book])))
    print([book.id for book in jack_only_book])

    # 查看jack_only_book实例对象
    for book in jack_only_book:
        print('delete前', book.__dict__)
        print(session.identity_map.__dict__)

    session.query(Author).filter(Author.name == 'jack').delete()
    session.query(Book).filter(Book.id.in_([book.id for book in jack_only_book])).delete(synchronize_session=False)

    # 查看jack_only_book实例对象
    for book in jack_only_book:
        print('commit前', book.__dict__)
        print(session.identity_map.__dict__)
        print('deleted', session.deleted)

    session.commit()
    # session.close()

    # 查看jack_only_book实例对象
    for book in jack_only_book:
        print('commit后', book.__dict__)
        print(session.identity_map.__dict__)
        print('deleted', session.deleted)

    print('上方使用了 synchronize_session 为False，然后没有更新 identity_map，那么在查询 new_book 时，是否会再次查找成功')
    # 不会查找成功，因为每一次查询，都会发送数据到数据库，将拿到的数据在 identify_map 中进行对比，查看是否已经存在该实例
    # 但是由于 id 3 已经被删除，在数据库中返回的是 None，则会直接返回 None，因为结果为None，没有必要再去比对 identify_map中的数据了。
    new_book = session.query(Book).filter_by(title='new_book').first()
    print('new_book', new_book)
    print(session.identity_map.__dict__)
    print('deleted', session.deleted)

    print('手动插入，发现上述的session.query会开启事务，下方使用con插入后，导致session找不到新数据'
          '原因是 MVCC 机制，所以需要在 con前，需要使用session.commit提交，让下一次的session.query是一个全新的饿事务')
    session.commit()

    # 手动插入一条 id 3 的数据，查看查找出得结果时 identify_map 还是con插入的数据

    with engine.connect() as con:
        sql = text('INSERT INTO books(id,title) VALUES(:id,:title)')
        con.execute(sql, [{'id': 3, 'title': 'insert_new_book'}, {'id': 4, 'title': 'four'}])
        con.commit()

    finish_book = session.query(Book).filter_by(id=3).first()
    four_book = session.query(Book).filter_by(id=4).first()
    print('finish_book', finish_book)
    print('four_book', four_book)
    print('finish_book', finish_book.__dict__)
    print(session.identity_map.__dict__)


def delete_by_cascade():
    session = session_factory()
    jack = session.query(Author).filter_by(id=1).first()
    print(jack)
    print(jack.__dict__)
    print(jack.books)
    # result = session.query(Author).filter(Author.id == jack.id).delete()
    # print('delresult', result)
    # session.commit()
    # print(session.identity_map.__dict__)
    # session.close()
    result = session.query(author_book, Book).join(Book, Author).all()
    print(result)


def create_instance_relationship():
    # 判断手动创建数据库中的实例对象，是否能否查找到 relationship 的关联实例
    # 总结：无法查找出来，原因是，如果直接创建实例，在使用 jack.books 是查找不出关联数据的，因为此时的jack没有跟数据库做关联。
    # 只有当实例跟session关联后，ORM才能正确的加载出关联数据，下方也可以使用 session.merge 同步jack跟数据库中的状态。
    # 如果 jack 没有跟session 关联，当使用 jack.books 时，SQLAlchemy会尝试通过 session 发出查询加载books数据，没有绑定session，则无法发出查询。
    jack = Author(name='jack', id=1)
    # print(jack.__dict__)
    # print(jack.books)
    session = session_factory()
    jack = session.merge(jack)
    print(jack.__dict__)
    print(jack.books)


def more_query_result_diff_data():
    session = session_factory()
    mary = Author(name='mary', fullname='jan_mary')
    session.add(mary)
    session.commit()
    session.close()


def more_query_result_diff():
    # 判断查询同一行记录，但是返回的列不同，session中的identity_map中的对象是否会改变，还是只会覆盖上一次的数据
    # 结论，当设置返回的具体列时，而不是整个类，返回的数据已不是实例对象，而是具体数据了。
    session = session_factory()
    result = session.query(Author.name).filter_by(name='mary').first()
    print(result)
    print(result.__dict__)
    print(session.identity_map)



if __name__ == "__main__":
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    # add_book()
    # add_to_jack()
    # search()
    # delete()
    # add_book_to_one()
    # delete_one()
    # delete_many_author_to_book()
    # delete_by_cascade()
    # create_instance_relationship()
    # more_query_result_diff_data()
    more_query_result_diff()
    # print(backref(backref('authors')))
