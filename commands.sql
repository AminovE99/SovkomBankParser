CREATE TABLE property_object(
  id SERIAL PRIMARY KEY,
  kadastr_num varchar(25),
  raw_address varchar(100),
  address varchar(100),
  link_of_kadastr_num varchar(100),
  floor varchar(20),
  json varchar(100000),
  square varchar(15),
  latitude float(15),
  longitude float(15)
);
SELECT count(*) AS nonull,
(SELECT count(*) FROM property_object WHERE json is NULL ) AS is_null
 FROM property_object WHERE json IS NOT NULL ; --Первый запрос

SELECT count(*) AS righted_raw_address FROM property_object WHERE raw_address = address -- Второй запрос