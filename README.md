# Water-pipe

A simple etl tool.

## Introduction

小水管，数据流

### Key features

- 迭代器导入导出

### TODO

- 实现hive/impala/greenplum的insert方法
- 扩展注册功能
- 进程池

## Install

pip install water-pipe

## Sample code

```python
from water_pipe.channel import DataChannel

if __name__=='__main__':
    impala_db_config = {
        "driver": "impala",
        "config": {
            "host": "127.0.01",
            "username": "admin",
            "password": "admin",
            "database": "default",
            "port": 21050,
            "auth_mechanism": "LDAP",
        }
    }
    pg_db_config = {
        "driver": "postgres",
        "config": {
            "host": "127.0.0.1",
            "username": "admin",
            "password": "admin",
            "database": "test",
            "port": 5432
        }
    }
    csv_db_config = {
        "driver": "csv",
        "config": {
            "filename": "data",
            # "path": ""
        }
    }

    with DataChannel(impala_db_config, pg_db_config) as channel:
        channel.table("tmp.t2")
        # channel.sink_db.execute("truncate table medical.t2")
        channel.insert("medical.t2", 2, is_create=True)
    
    with DataChannel(pg_db_config, impala_db_config) as channel:
        channel.query("select * from medical.t2 limit 9")
        channel.insert("tmp.t3", 2, is_create=True)
    
    with DataChannel(pg_db_config, csv_db_config) as channel: 
        channel.query("select * from medical.dim_date limit 123")
        channel.insert(is_create=True)
        
    with DataChannel(csv_db_config, pg_db_config) as channel: 
        channel.query()
        channel.insert("medical.t_csv", 2, is_create=True)
        
```

## Dependency

```shell
pip install loguru

pip install impyla
pip install psycopg
pip install psycopg-binary
pip install psycopg2
pip install mysqlclient
pip install openpyxl
```
