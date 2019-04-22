import psycopg2 as psycopg2

#TODO: Разделить одну таблицу на несколько


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
        conn = psycopg2.connect(host="localhost", database="postgres", user="postgres",
                                password="megavova")
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


def insert_unfoundable_word(json):
    sql = "INSERT INTO property_object(json) VALUES (%s)"
    conn = None
    try:
        conn = psycopg2.connect(host="localhost", database="postgres", user="postgres",
                                password="megavova")
        cur = conn.cursor()
        cur.execute(sql, (json,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
