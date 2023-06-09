from itertools import chain
import psycopg2
import re

from water_pipe.base import Connect, DTYPE

class PostgresConnect(Connect):
    
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
        
        self.connect = psycopg2.connect(**config)
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
        one_data = list(chain.from_iterable(data))  # 二维列表转一维列表
        # print(one_data)
        n_placeholders = ",".join([f"({self.placeholders})"] * len(data))
        # print(n_placeholders)
        self.cursor.execute("insert into {} values {}".format(table_name, n_placeholders), one_data)
        # self.cursor.executemany("insert into {} values ({})".format(table_name, self.placeholders), data)
    
    def set_query_schema(self, sql):
        type_sql = "select oid, typname from pg_type where oid < 10000"
        self.cursor.execute(type_sql)
        type_map = {}
        for row in self.cursor.fetchall():
            type_map[row[0]] = row[1]
        
        self.cursor.execute("select * from (" + sql + ") t limit 0")
        # https://www.psycopg.org/docs/cursor.html
        # 0.name: the name of the column returned.
        # 1.type_code: the PostgreSQL OID of the column.
        # 2.display_size: the actual length of the column in bytes.
        # 3.internal_size: the size in bytes of the column associated to this column on the server.
        # 4.precision: total number of significant digits in columns of type NUMERIC. None for other types.
        # 5.scale: count of decimal digits in the fractional part in columns of type NUMERIC. None for other types.
        # 6.null_ok: always None as not easy to retrieve from the libpq.
        for row in self.cursor.description:
            # print(row)  # Column(name='id', type_code=23)
            col_name = row[0]
            data_type = self.convert_std_dtype(DTYPE(type_map[row[1]], row[4], row[5]))
            comment = ""
            self.std_schema_data.append([col_name, data_type, comment])
        self.placeholders = ",".join(["%s"] * len(self.std_schema_data))
    
    def set_table_schema(self, table_name):
        # sql result: [col_name, col_type, precision, scale, column_comment, table_comment]
        sql = f"""
        select t1.column_name as col_name,
               t1.udt_name as col_type, 
               coalesce(t1.character_maximum_length, t1.numeric_precision) as precision,  
               t1.numeric_scale as scale,
               -- case when t1.udt_name like '%int%' then 'int'
               --      when t1.udt_name like '%float%' then 'float'
               --      when t1.udt_name like '%numeric%' then concat('numeric', 
               --                                                    case when t1.numeric_precision is null then '' else '(' || t1.numeric_precision end, 
               --                                                    case when t1.numeric_scale is null then '' else ',' || t1.numeric_scale || ')' end)
               --      when t1.udt_name like '%varchar%' then concat(t1.udt_name, 
               --                                                    case when t1.character_maximum_length is null then '' else '(' || t1.character_maximum_length || ')' end)
               --      when t1.udt_name like '%char%' then concat('char', 
               --                                                 case when t1.character_maximum_length is null then '' else '(' || t1.character_maximum_length || ')' end)
               --      else t1.udt_name::varchar end as data_type_str,             -- 字段类型(已转换的)
               t3.description as comment,
               t4.description as dataset_comment
	    from information_schema.columns t1
        join pg_catalog.pg_namespace pn on t1.table_schema = pn.nspname
        join pg_catalog.pg_class t2 on pn.oid = t2.relnamespace and t1.table_name = t2.relname 
        left join pg_catalog.pg_description t3 on t2.oid = t3.objoid and t1.ordinal_position = t3.objsubid
        left join pg_catalog.pg_description t4 on t2.oid = t4.objoid and t4.objsubid = 0
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
