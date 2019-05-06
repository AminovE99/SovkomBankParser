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

SELECT
  (SELECT count(*)
   FROM property_object
   WHERE raw_country IS NOT NULL) as is_not_null,
  (SELECT count(*)
   FROM property_object
   WHERE raw_country is NULL) as is_null; --Первое задание

SELECT (SELECT count(*)
        FROM property_object
        WHERE raw_region = handled_region AND raw_country = handled_country AND raw_city = handled_city AND
              raw_street = handled_street AND raw_house_num = handled_house_num AND raw_block = handled_block) --Второе задание

SELECT (SELECT count(*) FROM property_object WHERE )