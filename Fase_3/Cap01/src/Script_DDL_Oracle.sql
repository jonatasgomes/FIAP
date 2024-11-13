
-- Tabela Produtor
CREATE TABLE Produtor (
    id_produtor NUMBER PRIMARY KEY,
    nome VARCHAR2(255) NOT NULL,
    localizacao VARCHAR2(255)
);

-- Tabela Cultura
CREATE TABLE Cultura (
    id_cultura NUMBER PRIMARY KEY,
    nome VARCHAR2(255) NOT NULL,
    tipo VARCHAR2(255) NOT NULL,
    area NUMBER,
    id_produtor NUMBER,
    CONSTRAINT Cultura_Produtor_FK FOREIGN KEY (id_produtor) REFERENCES Produtor(id_produtor)
);

-- Tabela Insumo
CREATE TABLE Insumo (
    id_insumo NUMBER PRIMARY KEY,
    nome VARCHAR2(255) NOT NULL
);

-- Tabela Aplicacao
CREATE TABLE Aplicacao (
    id_aplicacao NUMBER PRIMARY KEY,
    id_cultura NUMBER NOT NULL,
    id_insumo NUMBER NOT NULL,
    data_hora DATE NOT NULL,
    quantidade NUMBER NOT NULL,
    CONSTRAINT Aplicacao_Cultura_FK FOREIGN KEY (id_cultura) REFERENCES Cultura(id_cultura),
    CONSTRAINT Aplicacao_Insumo_FK FOREIGN KEY (id_insumo) REFERENCES Insumo(id_insumo)
);

-- Tabela Sensor
CREATE TABLE Sensor (
    id_sensor NUMBER PRIMARY KEY,
    tipo_sensor VARCHAR2(255) NOT NULL,
    descricao VARCHAR2(255) NOT NULL
);

-- Tabela Leitura
CREATE TABLE Leitura (
    id_leitura NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_sensor NUMBER NOT NULL,
    id_cultura NUMBER NOT NULL,
    data_hora DATE NOT NULL,
    valor NUMBER,
    CONSTRAINT Leitura_Sensor_FK FOREIGN KEY (id_sensor) REFERENCES Sensor(id_sensor),
    CONSTRAINT Leitura_Cultura_FK FOREIGN KEY (id_cultura) REFERENCES Cultura(id_cultura)
);

-- Tabela Previsao
CREATE TABLE Previsao (
    id_previsao NUMBER PRIMARY KEY,
    id_cultura NUMBER NOT NULL,
    id_insumo NUMBER NOT NULL,
    data_previsao DATE NOT NULL,
    quantidade NUMBER NOT NULL,
    CONSTRAINT Previsao_Cultura_FK FOREIGN KEY (id_cultura) REFERENCES Cultura(id_cultura),
    CONSTRAINT Previsao_Insumo_FK FOREIGN KEY (id_insumo) REFERENCES Insumo(id_insumo)
);

-- Criar Dados
begin
  insert into Produtor (id_produtor, nome, localizacao) values (1, 'Fazenda Boa Colheita', 'Goiás');
  insert into Cultura (id_cultura, nome, tipo, area, id_produtor) values (1, 'Soja', 'Retângulo (ha)', '220', 1);
  insert into Cultura (id_cultura, nome, tipo, area, id_produtor) values (2, 'Milho', 'Retângulo (ha)', '500', 1);
  insert into Insumo (id_insumo, nome) values (1, 'Nitrogênio (N)');
  insert into Insumo (id_insumo, nome) values (2, 'Potássio (P)');
  insert into Insumo (id_insumo, nome) values (3, 'Fósforo (K)');
  insert into Sensor (id_sensor, tipo_sensor, descricao) values (1, 'Sensor de Nitrogênio', 'Sensor de Nitrogênio (N)');
  insert into Sensor (id_sensor, tipo_sensor, descricao) values (2, 'Sensor de Potássio', 'Sensor de Potássio (P)');
  insert into Sensor (id_sensor, tipo_sensor, descricao) values (3, 'Sensor de Fósforo', 'Sensor de Fósforo (K)');
  insert into Sensor (id_sensor, tipo_sensor, descricao) values (4, 'Sensor de pH', 'Sensor de pH');
  insert into Sensor (id_sensor, tipo_sensor, descricao) values (5, 'Sensor de Umidade', 'Sensor de Umidade');
  commit;
end;
/