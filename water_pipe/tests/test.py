
from water_pipe.channel import DataChannel

if __name__ == '__main__':
    impala_db_config = {
        "driver": "impala",
        "config": {
            "host": "10.63.82.218",
            "username": "work",
            "password": "TwkdFNAdS1nIikzk",
            "database": "default",
            "port": 21050,
            "auth_mechanism": "LDAP",
        }
    }
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
    mysql_db_config = {
        "driver": "mysql",
        "config": {
            "host": "10.63.82.207",
            "username": "test",
            "password": "test",
            "database": "tmp",
            "port": 3306
        }
    }
    csv_db_config = {
        "driver": "csv",
        "config": {
            "path": "e:/Codes/Python/water-pipe/water_pipe/tests/",
            "filename": "data.csv",
        }
    }
    excel_db_config = {
        "driver": "excel",
        "config": {
            "path": "e:/Codes/Python/water-pipe/water_pipe/tests/",
            "filename": "data.xlsx",
        }
    }
    # with DataChannel(impala_db_config, pg_db_config) as channel:
    #     channel.table("tmp.t2")
    #     channel.sink_db.execute("truncate table medical.t2")
    #     channel.insert("medical.t2", 2, is_create=True)
    
    # with DataChannel(pg_db_config, impala_db_config) as channel:
    #     channel.query("select * from medical.t2 limit 9")
    #     channel.insert("tmp.t3", 2, is_create=True)
    
    # with DataChannel(pg_db_config, csv_db_config) as channel:
    #     channel.query("select * from medical.dim_date limit 123")
    #     channel.insert(batch_size=10, is_create=True)
        
    # with DataChannel(csv_db_config, pg_db_config) as channel: 
    #     channel.query()
    #     channel.insert("medical.t_csv", 10, is_create=True)
    
    # with DataChannel(mysql_db_config, pg_db_config) as channel:
    #     channel.query("select * from tmp.t3 limit 9")
    #     channel.insert("medical.t3_copy", 2, is_create=True)
    
    with DataChannel(pg_db_config, excel_db_config) as channel:
        channel.query("select * from medical.dim_date limit 123")
        channel.insert(batch_size=10, is_create=True)
        
    # with DataChannel(excel_db_config, pg_db_config, ) as channel:
    #     channel.query()
    #     channel.insert("medical.t4_copy", 10, is_create=True)

