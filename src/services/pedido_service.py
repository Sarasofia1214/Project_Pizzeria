from src.config.database import db_instance
from datetime import datetime

class PedidoService:
    @staticmethod
    def crear_pedido(cliente_id, tipo, items, mesa=None):
        """
        tipo: 'tienda' o 'fuera'
        items: lista de {'producto_id': int, 'cantidad': int}
        """
        conn = db_instance.connect()
        cur = conn.cursor()
        try:
            conn.autocommit = False

            if tipo == 'tienda':
                cur.execute(
                    "INSERT INTO consumir_tienda (mesa) VALUES (%s) RETURNING id_consumir_tienda",
                    (mesa,)
                )
                consumo_tienda_id = cur.fetchone()[0]
                consumo_fuera_id = None
            else:
                cur.execute(
                    "INSERT INTO consumir_fuera (hora_pedido) VALUES (%s) RETURNING id_consumir_fuera",
                    (datetime.now(),)
                )
                consumo_tienda_id = None
                consumo_fuera_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO Pedidos (cliente, consumir_tienda, consumir_fuera, fecha, valor)
                VALUES (%s, %s, %s, %s, 0)
                RETURNING id_pedido
            """, (cliente_id, consumo_tienda_id, consumo_fuera_id, datetime.now()))
            pedido_id = cur.fetchone()[0]

            total = 0
            for item in items:
                cur.execute("SELECT precio_unitario FROM Productos WHERE id_menu = %s", (item['producto_id'],))
                precio = cur.fetchone()
                if not precio:
                    raise Exception(f"Producto {item['producto_id']} no encontrado")
                precio = precio[0]
                subtotal = precio * item['cantidad']
                total += subtotal

                cur.execute("""
                    INSERT INTO DetallePedido (pedido_id, producto_id, cantidad, precio_unitario)
                    VALUES (%s, %s, %s, %s)
                """, (pedido_id, item['producto_id'], item['cantidad'], precio))

            cur.execute("UPDATE Pedidos SET valor = %s WHERE id_pedido = %s", (total, pedido_id))

            conn.commit()
            print(f"✅ Pedido #{pedido_id} creado. Total: ${total:.2f}")
            return {'pedido_id': pedido_id, 'total': total}

        except Exception as e:
            conn.rollback()
            print(f"❌ Error al crear pedido: {e}")
            return None
        finally:
            conn.autocommit = True
            cur.close()
            db_instance.disconnect(conn)

    @staticmethod
    def listar_pedidos():
        conn = db_instance.connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT p.id_pedido, c.nombre, p.fecha, p.valor, p.estado
                FROM Pedidos p
                JOIN Cliente c ON p.cliente = c.id_cliente
                ORDER BY p.id_pedido DESC
            """)
            return cur.fetchall()
        finally:
            cur.close()
            db_instance.disconnect(conn)

    @staticmethod
    def obtener_pedido_completo(pedido_id):
        conn = db_instance.connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT p.id_pedido, c.nombre, p.fecha, p.valor, p.estado
                FROM Pedidos p
                JOIN Cliente c ON p.cliente = c.id_cliente
                WHERE p.id_pedido = %s
            """, (pedido_id,))
            pedido = cur.fetchone()
            if not pedido:
                return None

            cur.execute("""
                SELECT prod.pizzas, dp.cantidad, dp.precio_unitario
                FROM DetallePedido dp
                JOIN Productos prod ON dp.producto_id = prod.id_menu
                WHERE dp.pedido_id = %s
            """, (pedido_id,))
            detalles = cur.fetchall()

            return {
                'id': pedido[0],
                'cliente': pedido[1],
                'fecha': pedido[2],
                'total': float(pedido[3]),
                'estado': pedido[4],
                'detalles': [{'producto': d[0], 'cantidad': d[1], 'precio': float(d[2])} for d in detalles]
            }
        finally:
            cur.close()
            db_instance.disconnect(conn)

    @staticmethod
    def actualizar_estado(pedido_id, nuevo_estado):
        conn = db_instance.connect()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE Pedidos SET estado = %s WHERE id_pedido = %s", (nuevo_estado, pedido_id))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error: {e}")
            return False
        finally:
            cur.close()
            db_instance.disconnect(conn)