from persistence.db import get_connection
import pymysql

class Account:
    def __init__(self, id, number, creation_date, id_user):
        self.id = id
        self.number = number
        self.creation_date = creation_date
        self.id_user = id_user

    @staticmethod
    def check_account(id_user):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT number from account WHERE id_user = %s"
        cursor.execute(sql, (id_user,))

        row = cursor.fetchone()

        cursor.close()
        connection.close()
        return row is not None

    @staticmethod
    def get_by_user_id(id_user):
        connection = get_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT id, number, creation_date, id_user FROM account WHERE id_user = %s"
        cursor.execute(sql, (id_user,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        if row:
            return Account(row["id"], row["number"], row["creation_date"], row["id_user"])
        return None