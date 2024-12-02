"""
    理解 MetaData、Table、Column
    总结：
    1、在 SQLAlchemy 中，表示数据库元数据（元数据是指：数据库中的 表和列 的概念）的基础对象
        通常有，MetaData，Table，和Column
        MetaData：是（Table）对象的容器，存储了数据库中表的定义、列的信息、主键等其他信息，为整个数据库的表和关系提供了一个统一的视图
        Table：主要用于表示数据库中的表，Table对象定义了数据库表的结构，包括表的名称、列、主键、索引等信息，是基于MetaData数据库模式的基本单元
            Table 可以通过连接数据库，从数据库中的表反射加载表结构，保存在Table中,Table 中包含了 Column 和 Constraint对象。
            ORM 结构就是通过Table来实现 ORM 形式的查询等操作的
            通过 Table对象，提供了 SQL 生成的基础，可以找到数据库中的表以及表中的列，以及判断是否符合规则（类型是否错误）管理表之间的关系。
        Column：主要用来定义表中的列结构，描述表中的列的类型和约束，如：列的名称、数据类型、是否为主键、是否为null等。

"""
from sqlalchemy import MetaData, create_engine, Table, Column, String, Integer, ForeignKey

# 定义一个引擎，来连接数据库和维护连接池
engine = create_engine("mysql+pymysql://root:a123456789@localhost/demo")

# 创建一个集合，存储定义的表对象
meta_data = MetaData()

# 创建表对象（Table），同时需要将 metadata 传入，明确表所在的集合
user_table = Table('user_account', meta_data,
                   Column('id', Integer, primary_key=True, autoincrement=True),
                   Column('name', String(30), nullable=False),
                   Column('fullname', String(30)))

# print(user_table.c.keys())
print(user_table.columns)  # 获取表结构
print(user_table.primary_key)

# 创建 address 表结构（Table）
address_table = Table('address', meta_data, Column('id', Integer, primary_key=True, autoincrement=True),
                      Column('user_id', ForeignKey('user_account.id'), nullable=False),
                      Column('email_address', String(50), nullable=False))

# --------------通过反射，根据数据库中的表来生成Table对象
emp = Table('t_emp', meta_data, autoload_with=engine)

if __name__ == "__main__":
    # 将 meta 对象通过 engine 连接至数据库，如果数据库找不到该表则会自动根据Table对象内部的信息创建一张新表。
    # meta_data.create_all(engine)

    # 删除 meta 集合中的所有的 Table 对象
    # meta_data.drop_all(engine)
    print('demo', emp.c)
