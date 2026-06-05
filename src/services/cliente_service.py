from src.config.database import db_instance

class ClienteService:
    @staticmethod
    def crear_cliente(nombre, direccion, telefono):
        conn = db_instance.connect()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO Cliente (nombre, direccion, numero_telefono) VALUES (%s, %s, %s) RETURNING id_cliente",
                (nombre, direccion, telefono)
            )
            id_cliente = cur.fetchone()[0]
            conn.commit()
            print(f"✅ Cliente creado con ID: {id_cliente}")
            return id_cliente
        except Exception as e:
            conn.rollback()
            print(f"❌ Error: {e}")
            return None
        finally:
            cur.close()
            db_instance.disconnect(conn)

    @staticmethod
    def listar_clientes():
        conn = db_instance.connect()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id_cliente, nombre, direccion, numero_telefono FROM Cliente ORDER BY id_cliente")
            return cur.fetchall()
        finally:
            cur.close()
            db_instance.disconnect(conn)

    @staticmethod
    def actualizar_cliente(id_cliente, nombre=None, direccion=None, telefono=None):
        conn = db_instance.connect()
        cur = conn.cursor()
        try:
            updates = []
            params = []
            if nombre:
                updates.append("nombre = %s")
                params.append(nombre)
            if direccion:
                updates.append("direccion = %s")
                params.append(direccion)
            if telefono:
                updates.append("numero_telefono = %s")
                params.append(telefono)
            if not updates:
                return False
            params.append(id_cliente)
            query = f"UPDATE Cliente SET {', '.join(updates)} WHERE id_cliente = %s"
            cur.execute(query, params)
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"❌ Error: {e}")
            return False
        finally:
            cur.close()
            db_instance.disconnect(conn)

    @staticmethod
    def eliminar_cliente(id_cliente):
        conn = db_instance.connect()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM Cliente WHERE id_cliente = %s", (id_cliente,))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"❌ Error: {e}")
            return False
        finally:
            cur.close()
            db_instance.disconnect(conn)