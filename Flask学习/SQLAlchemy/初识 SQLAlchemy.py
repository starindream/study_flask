from sqlalchemy import create_engine, text

# print(sqlalchemy.__version__)

# engine 相当于是一个数据库连接池，在一个数据库服务器中只会创建一个连接池，创建engine不会直接建立连接
# 在具体的操作时（执行数据库任务），才会建立连接
engine = create_engine("mysql+pymysql://root:a123456789@localhost/demo")

# ************************ 使用 SQL 语句来操作数据库 *********************************

# 从连接池中获取连接，如果没有空闲连接，则创建一个新连接
# 上下文管理器创建了数据库连接，并在事务中进行操作
# Python DBAPI 的默认行为是在事务中进行的，结束时没有使用 con.commit提交，则会默认使用 rollback
with engine.connect() as con:
    # text 相当于是特定的 字符串 格式，提前将 SQL 语句进行转义，通过params传递进来的参数，不会被当作 SQL 进行词法分析
    result = con.execute(text("SELECT empno,ename FROM t_emp WHERE empno=:empno"), {'empno': 9000})
    # print('result', result.all())
    for res in result.mappings():
        print('res', res)

# connect 和 raw_connection 的区别是：一个是返回 SQLAlchemy 的连接对象，一个是返回底层数据库驱动的连接对象（不能使用 SQLAlchemy的语法）
# 使用 raw_connection，相当于直接返回了数据库驱动 pymysql 的连接对象
con = engine.raw_connection()
# 创建游标
cursor = con.cursor()
sql = 'SELECT * FROM t_emp WHERE empno=%s'
cursor.execute(sql, ['1 OR 1=1'])
print(cursor.fetchall())


# ----- 使用 connect commit 提交
def alchemy_commit():
    """ 使用 commit 提交信息 """
    with engine.connect() as con:
        sql = text("INSERT INTO t_emp(empno,ename) VALUES (:empno,:ename)")
        con.execute(sql, {'empno': 9009, 'ename': 'Alchemy'})
        # print('res', result.fetchall())
        con.commit()


# ----- 插入多条数据， 使用 begin 来进行提交，注意 begin 只能在 with 语句中使用：
def begin_alchemy():
    with engine.begin() as con:
        con.execute(text("INSERT INTO t_emp(empno,ename) VALUES (:empno,:ename)"),
                    [{'empno': 9998, 'ename': 'one'}, {'empno': 9999, 'ename': 'two'}])

    # con = engine.begin()
    # con.execute(text("INSERT INTO t_emp(empno,ename) VALUES (:empno,:ename)"), {'empno': 90190, 'ename': 'begin1'})
    pass


if __name__ == "__main__":
    # alchemy_commit()
    begin_alchemy()
    print('你好')
