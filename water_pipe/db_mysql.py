from itertools import chain
import MySQLdb

from water_pipe.base import Connect, DTYPE

class MysqlConnect(Connect):
        
    def __init__(self, norm_config) -> None:
        """
        norm_config = {
            "host": "127.0.0.1",
            "username": "admin",
            "password": "admin123",
            "database": "test",
            "port": 3306,
            ......
        }
        """
        config = norm_config.copy()
        config["user"] = config.pop("username")
        
        self.connect = MySQLdb.connect(**config)
        self.cursor = self.connect.cursor()
        
        self.std_schema_data = []
        self.dataset_comment = ""
        self.placeholders = ""
        
        self.dtype_map = {
            # 必须都要对应，且不存在的类型需要放在最下面
            "tinyint": ["tiny"],
            "int": ["int", "int24"],
            "bigint": ["bigint", "long"],
            "float": ["float"],
            "double": ["double"],
            "decimal": ["decimal", "newdecimal"],
            "char": ["char"],
            "varchar": ["varchar"],
            "text": ["text", "string"],
            "date": ["date"],
            "time": ["time"],
            "datetime": ["datetime"],
            "timestamp": ["timestamp"],
            # mysql不存在的数据类型
        }

    def execute(self, sql):
        self.cursor.execute(sql)
        
    def query(self, sql):
        self.set_query_schema(sql)
        self.cursor.execute(sql)
        return self.cursor.fetchmany

    def table(self, table_name):
        self.set_table_schema(table_name)
        self.cursor.execute(f"select * from {table_name}")
        return self.cursor.fetchmany
    
    def insert(self, table_name, data):
        # self.cursor.executemany("insert into {} values ({})".format(table_name, self.placeholders), data)
        
        one_data = list(chain.from_iterable(data))  # 二维列表转一维列表
        n_placeholders = ",".join([f"({self.placeholders})"] * len(data))
        self.cursor.execute("insert into {} values {}".format(table_name, n_placeholders), one_data)
    
    def set_query_schema(self, sql):
        ft = MySQLdb.constants.FIELD_TYPE
        type_map = {getattr(ft, k): k.lower() for k in dir(ft) if not k.startswith('_')}
        
        self.cursor.execute("select * from (" + sql + ") t limit 0")
        for row in self.cursor.description:
            # print(row)
            col_name = row[0]
            # data_type = self.convert_std_dtype(DTYPE(type_map[row[1]], row[4], row[5]))
            data_type = self.convert_std_dtype(DTYPE(type_map[row[1]]))
            comment = ""
            self.std_schema_data.append([col_name, data_type, comment])
        self.placeholders = ",".join(["%s"] * len(self.std_schema_data))
    
    def set_table_schema(self, table_name):
        # sql result: [col_name, col_type, precision, scale, column_comment, table_comment]
        sql = f"""
        select t1.column_name as col_name,
               t1.data_type as col_type, 
               coalesce(t1.character_maximum_length, t1.numeric_precision) as `precision`,  
               t1.numeric_scale as scale,
               t1.column_comment,
               t2.table_comment
	    from information_schema.columns as t1
	    join information_schema.tables t2 on t1.table_schema=t2.table_schema and t1.table_name=t2.table_name
	    where concat(t1.table_schema, '.', t1.table_name) = '{table_name}'
	    order by t1.ordinal_position
        """
        self.cursor.execute(sql)
        for row in self.cursor.fetchall():
            col_name = row[0]
            data_type = self.convert_std_dtype(DTYPE(row[1], row[2], row[3]))
            comment = row[4]
            self.std_schema_data.append([col_name, data_type, comment])
            self.dataset_comment = row[5]
        self.placeholders = ",".join(["%s"] * len(self.std_schema_data))
    
    def create_table(self, table_name):
        cols_list = []
        cols_comment_list = []
        for row in self.std_schema_data:
            col_name = row[0]
            # dtype = self.convert_self_dtype(row[1])
            data_type = self.convert_self_dtype(row[1]).get()
            comment = row[2]
            cols_list.append("    {:<30} {}".format(col_name, data_type))
            if comment:
                cols_comment_list.append(f"\ncomment on column {table_name}.{col_name} is '{comment}';")
        
        sql = f"create table if not exists {table_name} (\n" + \
            ",\n".join(cols_list) + \
            "\n);"
        if self.dataset_comment:
            sql += f"\ncomment on table {table_name} is '{self.dataset_comment}';"
        if cols_comment_list:
            sql += "".join(cols_comment_list)
        print(sql)
        self.cursor.execute(sql)