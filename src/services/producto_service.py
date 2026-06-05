from src.config.database import db_instance

class ProductoService:
    @staticmethod
    def listar_productos():
        conn = db_instance.connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id_menu, pizzas, panzerottis, bebidas, postres, precio_unitario 
                FROM Productos 
                WHERE disponible = true
                ORDER BY id_menu
            """)
            return cur.fetchall()
        finally:
            cur.close()
            db_instance.disconnect(conn)

    @staticmethod
    def obtener_producto(id_menu):
        conn = db_instance.connect()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id_menu, pizzas, precio_unitario FROM Productos WHERE id_menu = %s", (id_menu,))
            return cur.fetchone()
        finally:
            cur.close()
            db_instance.disconnect(conn)

    @staticmethod
    def actualizar_precio(id_menu, nuevo_precio):
        conn = db_instance.connect()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE Productos SET precio_unitario = %s WHERE id_menu = %s", (nuevo_precio, id_menu))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error: {e}")
            return False
        finally:
            cur.close()
            db_instance.disconnect(conn)