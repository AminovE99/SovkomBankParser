# SovkomParser
Парсер, который может в базу данных занести данные с сайта https://egrp365.ru/
#### На вход подается: Адрес
#### На выходе ожидается: 


# Чтобы пользоваться:
### 1.Создайте Базу данных:
```
CREATE TABLE property_object (
  id                  SERIAL PRIMARY KEY,
  kadastr_num         varchar(25),
  postal_code         varchar(6),
  raw_country         varchar(40),
  raw_region          varchar(40),
  raw_city            varchar(40),
  raw_street          varchar(40),
  raw_house_num       varchar(6),
  raw_block           integer,
  raw_flat            integer,
  handled_country     varchar(40),
  handled_region      varchar(40),
  handled_city        varchar(40),
  handled_street      varchar(50),
  handled_house_num   varchar(6),
  handled_block       integer,
  handled_flat        integer,
  link_of_kadastr_num varchar(100),
  floor               integer,
  square              float(16),
  latitude            float(15),
  longitude           float(15)
);
```
### 2. Скачайте все библиотеки с requirements.txt
### 3. Запустите файл parser.py
