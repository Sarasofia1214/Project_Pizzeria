"""
Servicio para la entidad Productos (bicicletas, repuestos, etc.).
"""

from src.config.database import dbInstance

class ProductoService:
    """Operaciones relacionadas con productos."""

    @staticmethod
    def getAllProducts():
        """Retorna todos los productos con id, tipo, stock, precio y detalles."""
        conn = dbInstance.connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id_producto, tipo, cantidad_producto, precio_unitario, detalles
                FROM Productos
                ORDER BY id_producto
            """)
            return cur.fetchall()
        finally:
            cur.close()
            dbInstance.disconnect(conn)

    @staticmethod
    def getProductById(productId):
        """Retorna un solo producto o None."""
        conn = dbInstance.connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT id_producto, tipo, cantidad_producto, precio_unitario, detalles
                FROM Productos
                WHERE id_producto = %s
            """, (productId,))
            return cur.fetchone()
        finally:
            cur.close()
            dbInstance.disconnect(conn)

    @staticmethod
    def updateProductPrice(productId, newPrice):
        """Actualiza el precio unitario de un producto."""
        conn = dbInstance.connect()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE Productos SET precio_unitario = %s WHERE id_producto = %s",
                        (newPrice, productId))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"❌ Error al actualizar precio: {e}")
            return False
        finally:
            cur.close()
            dbInstance.disconnect(conn)

    @staticmethod
    def updateProductStock(productId, newStock):
        """Actualiza la cantidad disponible en stock."""
        conn = dbInstance.connect()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE Productos SET cantidad_producto = %s WHERE id_producto = %s",
                        (newStock, productId))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"❌ Error al actualizar stock: {e}")
            return False
        finally:
            cur.close()
            dbInstance.disconnect(conn)