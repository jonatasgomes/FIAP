create or replace view nivel_agua as
select to_char(data_leitura, 'YYYY-MM-DD HH24:MI:SS') as data_leitura, valor
  from sensor_leituras l
 where sensor = 'RIO'
 order by l.data_leitura desc
 fetch first row only
/

create or replace view volume_chuva as
select to_char(data_leitura, 'YYYY-MM-DD HH24:MI:SS') as data_leitura, valor
  from sensor_leituras l
 where sensor = 'CHUVA'
 order by l.data_leitura desc
 fetch first row only
/

select * from nivel_agua;
select * from volume_chuva;
