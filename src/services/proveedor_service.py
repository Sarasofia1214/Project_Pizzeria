"""
Servicio para Proveedores.
"""
from src.config.database import dbInstance

class ProveedorService:
    @staticmethod
    def getAllProveedores():
        """Retorna todos los proveedores."""
        conn = dbInstance.connect()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id_proveedor, nombre, direccion, telefono, email, pais FROM Proveedores ORDER BY id_proveedor")
            return cur.fetchall()
        finally:
            cur.close()
            dbInstance.disconnect(conn)