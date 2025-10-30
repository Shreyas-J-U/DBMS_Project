import pymysql
from pymysql import Error


def add_store(db_resources, store_data):
    """
    store_data = (store_name, location_dict, manager_id)
    location_dict = {"lat": float, "lng": float}
    """
    connection, cursor = db_resources

    try:
        store_name, location, manager_id = store_data
        lat = location["lat"]
        lng = location["lng"]

        query = """
            INSERT INTO store (store_name, location, manager_id)
            VALUES (%s, ST_GeomFromText(%s), %s);
        """
        point_str = f'POINT({lng} {lat})'  # MySQL expects POINT(longitude latitude)

        cursor.execute(query, (store_name, point_str, manager_id))
        connection.commit()
        return True

    except Exception as e:
        print("Error inserting store:", e)
        connection.rollback()
        return False



def remove_store(db_resources,store_id):
    
    connection,cursor = db_resources
    try:
        query = "DELETE FROM store WHERE store_id = %s"
        cursor.execute(query,store_id)
        connection.commit()
        return True
    except Exception as e:
        print(e)
        connection.rollback()
        return False