"""
Servicio para la entidad Cliente.
Proporciona operaciones CRUD.
"""

from src.config.database import dbInstance

class ClienteService:
    """Maneja todas las operaciones de base de datos para clientes."""

    @staticmethod
    def createCustomer(nombre, direccion, telefono, saldoActual=0.0):
        """
        Inserta un nuevo cliente.
        Retorna el ID del nuevo cliente o None en caso de error.
        """
        conn = dbInstance.connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO Cliente (nombre, direccion, numero_telefono, saldo_actual)
                VALUES (%s, %s, %s, %s)
                RETURNING id_cliente
            """, (nombre, direccion, telefono, saldoActual))
            customerId = cur.fetchone()[0]
            conn.commit()
            print(f"✅ Cliente creado con ID: {customerId}")
            return customerId
        except Exception as e:
            conn.rollback()
            print(f"❌ Error al crear cliente: {e}")
            return None
        finally:
            cur.close()
            dbInstance.disconnect(conn)

    @staticmethod
    def getAllCustomers():
        """Retorna todos los clientes como lista de tuplas."""
        conn = dbInstance.connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id_cliente, nombre, direccion, numero_telefono, saldo_actual
                FROM Cliente
                ORDER BY id_cliente
            """)
            return cur.fetchall()
        finally:
            cur.close()
            dbInstance.disconnect(conn)

    @staticmethod
    def getCustomerById(customerId):
        """Retorna un cliente por su ID o None."""
        conn = dbInstance.connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id_cliente, nombre, direccion, numero_telefono, saldo_actual
                FROM Cliente
                WHERE id_cliente = %s
            """, (customerId,))
            return cur.fetchone()
        finally:
            cur.close()
            dbInstance.disconnect(conn)

    @staticmethod
    def updateCustomer(customerId, nombre=None, direccion=None, telefono=None, saldoActual=None):
        """
        Actualiza los campos de un cliente. Solo se actualizan los proporcionados.
        Retorna True si al menos una fila fue actualizada.
        """
        conn = dbInstance.connect()
        cur = conn.cursor()
        try:
            updates = []
            params = []
            if nombre is not None:
                updates.append("nombre = %s")
                params.append(nombre)
            if direccion is not None:
                updates.append("direccion = %s")
                params.append(direccion)
            if telefono is not None:
                updates.append("numero_telefono = %s")
                params.append(telefono)
            if saldoActual is not None:
                updates.append("saldo_actual = %s")
                params.append(saldoActual)
            if not updates:
                return False
            params.append(customerId)
            query = f"UPDATE Cliente SET {', '.join(updates)} WHERE id_cliente = %s"
            cur.execute(query, params)
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"❌ Error al actualizar cliente: {e}")
            return False
        finally:
            cur.close()
            dbInstance.disconnect(conn)

    @staticmethod
    def deleteCustomer(customerId):
        """Elimina un cliente. Retorna True si se eliminó."""
        conn = dbInstance.connect()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM Cliente WHERE id_cliente = %s", (customerId,))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"❌ Error al eliminar cliente: {e}")
            return False
        finally:
            cur.close()
            dbInstance.disconnect(conn)