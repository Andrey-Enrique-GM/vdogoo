import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="chihuahua",
        database="dogodb",
        port=3307
    )