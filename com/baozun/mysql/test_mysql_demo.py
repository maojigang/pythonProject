import pymysql
from pymysql.err import OperationalError, ProgrammingError
def get_mysql_connection():
    """创建并返回 MySQL 连接对象"""
    try:
        conn = pymysql.connect(
            host='w-kh-ross-sit-mysql.service.testdb',    # 数据库地址（本地填 127.0.0.1，远程填服务器IP）
            port=3306,           # 端口（MySQL 默认 3306）
            user='u_ddc_pem_sit',         # 用户名
            password='u_ddc_pem_sit1234',  # 密码（替换为你的实际密码）
            database='db_ddc_pem_sit',  # 要连接的数据库名（需提前创建）
            charset='utf8mb4'    # 字符集（支持 emoji 等特殊字符）
        )
        return conn
    except OperationalError as e:
        print(f"连接失败：{e}")
        return None


def query_data():
    conn = get_mysql_connection()
    if not conn:
        return

    try:
        # 创建游标（cursorclass=pymysql.cursors.DictCursor 使结果以字典返回，更易读）
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            # 执行 SQL 查询
            sql = "select id, create_time , pf_doc_no from my_table  where id < %s"
            cursor.execute(sql, (18,))  # 使用参数化查询，避免 SQL 注入

            # 获取结果：fetchone() 单条 / fetchall() 所有 / fetchmany(5) 指定条数
            results = cursor.fetchall()
            print("查询结果：")
            for row in results:
                print(f"ID: {row['id']}, 时间: {row['create_time']}, 商品编码: {row['pf_doc_no']}")
    except ProgrammingError as e:
        print(f"查询失败：{e}")
    finally:
        conn.close()  # 确保连接关闭

def test_mysql1():
    query_data()
    pass


if __name__ == '__main__':
    test_mysql1()


