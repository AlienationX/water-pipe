from itertools import chain
import psycopg
import re

from water_pipe.db_postgres import PostgresConnect

class GreenplumConnect(PostgresConnect):
    """
    https://www.psycopg.org/psycopg3/docs/basic/copy.html#copy
    
    使用 psycopg3 新版api, 支持copy等新功能, 但效率好像并不高
    该链接推荐使用继承的方式来扩展未实现的数据库, 或覆写效率不高的方法
    """
    
    def __init__(self, norm_config) -> None:
        """
        norm_config = {
            "host": "127.0.0.1",
            "username": "admin",
            "password": "admin123",
            "database": "test",
            "port": 5432,
            ......
        }
        """
        config = norm_config.copy()
        config["user"] = config.pop("username")
        config["dbname"] = config.pop("database")
        
        self.connect = psycopg.connect(**config)
        self.cursor = self.connect.cursor()
        
        self.std_schema_data = []
        self.dataset_comment = ""
        self.placeholders = ""
        
        self.dtype_map = {
            # 必须都要对应，且不存在的类型需要放在最下面
            "tinyint": ["int2"],
            "int": ["int4"],
            "bigint": ["int8"],
            "float": ["float"],
            "double": ["float"],
            "decimal": ["numeric"],
            "char": ["char"],
            "varchar": ["varchar"],
            "text": ["text"],
            "date": ["date"],
            "time": ["time"],
            "timestamp": ["timestamp"],
            # postgres不存在的数据类型
            "datetime": ["timestamp"],
        }
    
    def insert(self, table_name, data):
        """
        records = [(10, 20, "hello"), (40, None, "world")]

        with cursor.copy("COPY sample (col1, col2, col3) FROM STDIN (FORMAT TEXT)") as copy:
            for record in records:
                copy.write_row(record)
        """
        
        with self.cursor.copy(f"COPY {table_name} FROM STDIN") as copy:
            for record in data:
                copy.write_row(record)
        
        # data_str = "\n".join([ "\t".join([str(a) for a in x]) for x in data]) + "\n"  # 末尾一定要再加一个换行，否则报错
        # data_text = data_str.encode()
        # with self.cursor.copy(f"COPY {table_name} FROM STDIN") as copy:
        #     copy.write(data_text)
        

if __name__ == "__main__":
    pg_db_config = {
        "driver": "postgres",
        "config": {
            "host": "10.63.82.191",
            "username": "dw_rw",
            "password": "Yxsj@123",
            "database": "test",
            "port": 5432
        }
    }
    # gp = GreenplumConnect(pg_db_config["config"])
    # data = [(10, 20, "hello"), (40, None, "world") ]
    # gp.insert('medical.ttt', data)
    # gp.connect.commit()
    
    conn = psycopg.connect("dbname=test user=dw_rw host=10.63.82.191 port=5432")
    cursor = conn.cursor()
    
    records = [(10, 20, "hello world"), (40, None, "i'm beijing")]
    
    records_str = "\n".join([ "\t".join([str(a) for a in x]) for x in records]) + "\n"  # 末尾一定要再加一个换行，否则报错
    records_text = records_str.encode()
    
    sample_text = b"""\
40010\t40020\thello
40040\t\\N\tworld
"""
    print(records_text)
    print(sample_text)

    with cursor.copy("COPY medical.ttt (id, name, addr) FROM STDIN") as copy:
        for record in records:
            copy.write_row(record)
        # copy.write(sample_text)
        # copy.write(records_text)

    cursor.close()
    conn.commit()
    conn.close()
    