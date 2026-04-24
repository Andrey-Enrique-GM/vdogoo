from enums.value_permission import ValuePermission
from persistence.db import get_connection
import pymysql

class Permission ():
    def __init__(self, id: int, value: ValuePermission):
        self.id = id
        self.value = value


    # Obtiene los permisos de un usuario especificado por su id
    def get_permissions_by_user(id_user):
        try:
            connection = get_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            
            sql = "SELECT id, value FROM permission WHERE id_user = %s"
            cursor.execute(sql, (id_user,))
            
            rows = cursor.fetchall()
            
            permissions = []
            for row in rows:
                permissions.append(Permission(
                    row["id"], 
                    row["value"]
                ))
            
            cursor.close()
            connection.close()
            return permissions
        except Exception as ex:
            print(f"Error consultan permisos: {ex}")
            return []
