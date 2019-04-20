import psycopg2 as psycopg2


def insert_words_list(kadastr_num, address, link_of_kadastr_num, floor, json,square,lat,long):
    sql = "INSERT INTO property_object(kadastr_num, adress, link_of_kadastr_num, json, floor, square,latitude,longitude) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    conn = None
    try:
        conn = psycopg2.connect(host="localhost", database="postgres", user="postgres",
                                password="megavova")
        cur = conn.cursor()
        cur.execute(sql, (kadastr_num, address, link_of_kadastr_num,json,floor,square,float(lat),float(long)))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
