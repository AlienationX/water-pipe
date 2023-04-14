from itertools import chain
import psycopg
import re

from water_pipe.base import Connect, DTYPE

class GreenplumConnect(Connect):
    """使用 psycopg3 新版api，支持copy等新功能"""
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
        
        self.connect = psycopg.connect(**config)
        self.cursor = self.connect.cursor()
        
        self.std_schema_data = []
        self.dataset_comment = ""
        self.placeholders = ""
        
        self.dtype_map = {
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