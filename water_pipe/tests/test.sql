create table tmp.t2 (
id int,
name varchar(20),
address string,
birthday timestamp,
fee decimal(32,4)
);

insert overwrite table tmp.t2 
select 1 as id, cast('aa' as varchar(20)) as name, 'beijing'  as address, '2020-01-01 12:23:44' as birthday, null as fee union all
select 2 as id, cast('bb' as varchar(20)) as name, 'shanghai' as address, '2020-01-02 02:23:44' as birthday, 0 as fee union all
select 3 as id, cast('aa' as varchar(20)) as name, 'beijing'  as address, '2020-01-03 02:23:4' as birthday, 22.3 as fee
;