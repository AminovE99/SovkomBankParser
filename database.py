import psycopg2 as psycopg2


# TODO: Разделить одну таблицу на несколько (или подумать, как это сделать без словарей или хардкода)

HOST = "localhost"
DATABASE = "postgres"
USER = "postgres"
PASSWORD = "megavova"

def insert_words_list(kadastr_num,
                      postal_code,
                      raw_country,
                      raw_region,
                      raw_city,
                      raw_street,
                      raw_house_num,
                      raw_block,
                      raw_flat,
                      handled_country,
                      handled_region,
                      handled_city,
                      handled_street,
                      handled_house_num,
                      handled_block,
                      handled_flat,
                      link_of_kadastr_num,
                      floor,
                      json,
                      square,
                      latitude,
                      longitude):
    sql = ''' 
    INSERT INTO property_object(
    kadastr_num,
    postal_code,
    raw_country,
    raw_region,
    raw_city,
    raw_street,
    raw_house_num,
    raw_block,
    raw_flat,
    handled_country,
    handled_region,
    handled_city,
    handled_street,
    handled_house_num,
    handled_block,
    handled_flat,
    link_of_kadastr_num,
    floor,
    json,
    square,
    latitude,
    longitude) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
    '''
    conn = None
    try:
        conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER,
                                password=PASSWORD)
        cur = conn.cursor()
        cur.execute(sql, (
            kadastr_num,
            postal_code,
            raw_country,
            raw_region,
            raw_city,
            raw_street,
            raw_house_num,
            raw_block,
            raw_flat,
            handled_country,
            handled_region,
            handled_city,
            handled_street,
            handled_house_num,
            handled_block,
            handled_flat,
            link_of_kadastr_num,
            floor,
            json,
            square,
            latitude,
            longitude))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_unfoundable_word(handled_country, handled_region, handled_city, handled_street, handled_house_num,
                            handled_block, handled_flat):
    sql = '''INSERT INTO property_object(handled_country,
handled_region,
handled_city,
handled_street,
handled_house_num,
handled_block,
handled_flat) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
    conn = None
    try:
        conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER,
                                password=PASSWORD)
        cur = conn.cursor()
        cur.execute(sql, (handled_country, handled_region, handled_city,handled_street,handled_house_num,handled_block,handled_flat))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
