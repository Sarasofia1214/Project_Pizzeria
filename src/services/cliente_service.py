
import re
from src.config.database import dbInstance

class ClienteService:
    """Maneja todas las operaciones de base de datos para clientes."""

    @staticmethod
    def _validarNombre(nombre):
        """Valida que el nombre solo contenga letras, espacios y caracteres comunes."""
        if not nombre or len(nombre.strip()) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres.")
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]+$", nombre):
            raise ValueError("El nombre solo puede contener letras, espacios y acentos.")
        return nombre.strip().title()

    @staticmethod
    def _validarDireccion(direccion):
        """Valida dirección: letras, números, espacios, guiones, puntos."""
        if not direccion or len(direccion.strip()) < 3:
            raise ValueError("La dirección debe tener al menos 3 caracteres.")
        if not re.match(r"^[a-zA-Z0-9áéíóúÁÉÍÓÚüÜñÑ\s\.\-]+$", direccion):
            raise ValueError("La dirección contiene caracteres no permitidos.")
        return direccion.strip()

    @staticmethod
    def _validarTelefono(telefono):
        """Valida que el teléfono contenga solo dígitos y tenga entre 7 y 15 caracteres."""
        if not telefono:
            return None  # El teléfono puede ser opcional
        telefono_str = str(telefono).strip()
        if not telefono_str.isdigit():
            raise ValueError("El teléfono debe contener solo números.")
        if len(telefono_str) < 7 or len(telefono_str) > 15:
            raise ValueError("El teléfono debe tener entre 7 y 15 dígitos.")
        return telefono_str

    @staticmethod
    def _validarSaldo(saldo):
        """Valida que el saldo sea un número no negativo."""
        try:
            saldo = float(saldo)
            if saldo < 0:
                raise ValueError("El saldo no puede ser negativo.")
            return saldo
        except (ValueError, TypeError):
            raise ValueError("El saldo debe ser un número válido.")

    @staticmethod
    def createCustomer(nombre, direccion, telefono, saldoActual=0.0):
        """
        Inserta un nuevo cliente con validaciones.
        Retorna el ID del nuevo cliente o None en caso de error.
        """
        # Validaciones
        try:
            nombreValidado = ClienteService._validarNombre(nombre)
            direccionValidada = ClienteService._validarDireccion(direccion)
            telefonoValidado = ClienteService._validarTelefono(telefono)
            saldoValidado = ClienteService._validarSaldo(saldoActual)
        except ValueError as e:
            print(f"❌ Error de validación: {e}")
            return None

        conn = dbInstance.connect()
        cur = conn.cursor()
        try:
            # Usamos la secuencia correctamente, sin especificar id_cliente
            cur.execute("""
                INSERT INTO Cliente (nombre, direccion, numero_telefono, saldo_actual)
                VALUES (%s, %s, %s, %s)
                RETURNING id_cliente
            """, (nombreValidado, direccionValidada, telefonoValidado, saldoValidado))
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
        Aplica las mismas validaciones.
        Retorna True si al menos una fila fue actualizada.
        """
        updates = []
        params = []
        try:
            if nombre is not None:
                nombreValidado = ClienteService._validarNombre(nombre)
                updates.append("nombre = %s")
                params.append(nombreValidado)
            if direccion is not None:
                direccionValidada = ClienteService._validarDireccion(direccion)
                updates.append("direccion = %s")
                params.append(direccionValidada)
            if telefono is not None:
                telefonoValidado = ClienteService._validarTelefono(telefono)
                updates.append("numero_telefono = %s")
                params.append(telefonoValidado)
            if saldoActual is not None:
                saldoValidado = ClienteService._validarSaldo(saldoActual)
                updates.append("saldo_actual = %s")
                params.append(saldoValidado)
            if not updates:
                return False
            params.append(customerId)
        except ValueError as e:
            print(f"❌ Error de validación: {e}")
            return False

        conn = dbInstance.connect()
        cur = conn.cursor()
        try:
            query = f"UPDATE Cliente SET {', '.join(updates)} WHERE id_cliente = %s"
            cur.execute(query, params)
            conn.commit()
            if cur.rowcount > 0:
                print("✅ Cliente actualizado correctamente.")
            else:
                print("⚠️ No se encontró el cliente o no se realizaron cambios.")
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
            if cur.rowcount > 0:
                print("✅ Cliente eliminado.")
                return True
            else:
                print("⚠️ Cliente no encontrado.")
                return False
        except Exception as e:
            conn.rollback()
            print(f"❌ Error al eliminar cliente: {e}")
            return False
        finally:
            cur.close()
            dbInstance.disconnect(conn)