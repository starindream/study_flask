from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# 创建引擎（相当于数据库连接）
engine = create_engine('mysql+pymysql://root:a123456789@localhost/demo')


# ———————————————————— 使用 ORM 发送原生 SQL 语句

def session_sql():
    """ 使用 ORM 中的 session 来发送原声的 SQL 语句"""
    with Session(engine) as session:
        # 使用 text 将sql语句进行二进制转义，让后续占位符传入的字符，不拥有SQL词法分析。
        sql = text("SELECT empno,ename FROM t_emp WHERE empno>:empno")
        result = session.execute(sql, {'empno': 9000})
        print('result', result)
        for one in result:
            print(one.empno)


def session_sql_insert():
    with Session(bind=engine) as session:
        sql = text("INSERT INTO t_emp(empno,ename) VALUES(:empno,:ename)")
        session.execute(sql, [{'empno': 1001, 'ename': 'name-1001'}, {'empno': 1002, 'ename': 'name-1002'}])
        session.commit()


if __name__ == '__main__':
    # session_sql()
    session_sql_insert()
