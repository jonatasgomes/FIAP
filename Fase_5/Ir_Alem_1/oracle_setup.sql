create table sensor_leituras (
  id number not null,
  data_leitura date not null,
  sensor varchar2(128) not null,
  valor number,
  constraint sensor_leituras_pk primary key (id)
);

create or replace trigger sensor_leituras_bi_trg
  before insert on sensor_leituras for each row
begin
  if :new.id is null then
    select nvl(max(id), 0) + 1
      into :new.id
      from sensor_leituras;
  end if;
end sensor_leituras_bi_trg;
/

select * from sensor_leituras;

-- https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap/leituras/
-- https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap/leituras/1
