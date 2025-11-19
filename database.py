import sqlite3
import psycopg2
import psycopg2.extras
from datetime import datetime
import secrets
import os

def get_db_connection():
    """Obtener conexión a la base de datos (PostgreSQL en producción, SQLite en desarrollo)"""
    database_url = os.environ.get('DATABASE_URL')

    if database_url:
        # PostgreSQL en producción (Render)
        conn = psycopg2.connect(database_url)
        # Usar RealDictCursor para obtener resultados como diccionarios
        return conn
    else:
        # SQLite en desarrollo local
        conn = sqlite3.connect('caec.db')
        conn.row_factory = sqlite3.Row
        return conn

def get_cursor(conn):
    """Obtener cursor apropiado según el tipo de base de datos"""
    if is_postgres():
        return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    else:
        return conn.cursor()

def is_postgres():
    """Verificar si estamos usando PostgreSQL"""
    return os.environ.get('DATABASE_URL') is not None

def dict_from_row(row):
    """Convertir una fila de base de datos a diccionario"""
    if row is None:
        return None
    if is_postgres():
        # PostgreSQL con psycopg2 - row es tupla, necesitamos los nombres de columnas
        return row
    else:
        # SQLite - row_factory ya lo convierte a dict-like
        return dict(row)

def init_db():
    """Inicializar la base de datos con las tablas necesarias"""
    conn = get_db_connection()
    cursor = get_cursor(conn)

    # Detectar si es PostgreSQL o SQLite
    use_postgres = is_postgres()

    # Tabla de usuarios
    if use_postgres:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuario (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ultimo_acceso TIMESTAMP,
                activo BOOLEAN DEFAULT TRUE
            )
        ''')
    else:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                ultimo_acceso DATETIME,
                activo BOOLEAN DEFAULT 1
            )
        ''')

    # Tabla de contacto
    if use_postgres:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacto (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER NOT NULL,
                telefono VARCHAR(20),
                celular VARCHAR(20),
                direccion TEXT,
                ciudad VARCHAR(100),
                pais VARCHAR(100),
                codigo_postal VARCHAR(20),
                FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE
            )
        ''')
    else:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                telefono VARCHAR(20),
                celular VARCHAR(20),
                direccion TEXT,
                ciudad VARCHAR(100),
                pais VARCHAR(100),
                codigo_postal VARCHAR(20),
                FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE
            )
        ''')

    # Tabla de sistemas CAEC
    if use_postgres:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sistema_caec (
                id SERIAL PRIMARY KEY,
                codigo_sistema VARCHAR(50) UNIQUE NOT NULL,
                usuario_id INTEGER,
                nombre_sistema VARCHAR(100),
                fecha_vinculacion TIMESTAMP,
                ultimo_sync TIMESTAMP,
                estado VARCHAR(20) DEFAULT 'activo',
                modelo VARCHAR(50),
                version_firmware VARCHAR(20),
                FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE SET NULL
            )
        ''')
    else:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sistema_caec (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_sistema VARCHAR(50) UNIQUE NOT NULL,
                usuario_id INTEGER,
                nombre_sistema VARCHAR(100),
                fecha_vinculacion DATETIME,
                ultimo_sync DATETIME,
                estado VARCHAR(20) DEFAULT 'activo',
                modelo VARCHAR(50),
                version_firmware VARCHAR(20),
                FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE SET NULL
            )
        ''')

    # Tabla de datos de sensores (histórico)
    if use_postgres:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id SERIAL PRIMARY KEY,
                sistema_id INTEGER NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                nivel_agua REAL,
                ph REAL,
                temperatura REAL,
                nivel_nutrientes REAL,
                irrigacion_activa BOOLEAN,
                luz_activa BOOLEAN,
                FOREIGN KEY (sistema_id) REFERENCES sistema_caec(id) ON DELETE CASCADE
            )
        ''')
    else:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sistema_id INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                nivel_agua REAL,
                ph REAL,
                temperatura REAL,
                nivel_nutrientes REAL,
                irrigacion_activa BOOLEAN,
                luz_activa BOOLEAN,
                FOREIGN KEY (sistema_id) REFERENCES sistema_caec(id) ON DELETE CASCADE
            )
        ''')

    # Insertar sistemas CAEC de ejemplo para pruebas
    if use_postgres:
        # PostgreSQL usa ON CONFLICT en lugar de INSERT OR IGNORE
        cursor.execute('''
            INSERT INTO sistema_caec
            (codigo_sistema, nombre_sistema, estado, modelo, version_firmware)
            VALUES
            ('CAEC-2024-0001', 'Sistema Demo 1', 'disponible', 'CAEC-V1', '1.0.0'),
            ('CAEC-2024-0002', 'Sistema Demo 2', 'disponible', 'CAEC-V1', '1.0.0'),
            ('CAEC-2024-0003', 'Sistema Demo 3', 'disponible', 'CAEC-V2', '1.2.0'),
            ('CAEC-2024-TEST', 'Sistema Test', 'disponible', 'CAEC-V1', '1.0.0')
            ON CONFLICT (codigo_sistema) DO NOTHING
        ''')
    else:
        cursor.execute('''
            INSERT OR IGNORE INTO sistema_caec
            (codigo_sistema, nombre_sistema, estado, modelo, version_firmware)
            VALUES
            ('CAEC-2024-0001', 'Sistema Demo 1', 'disponible', 'CAEC-V1', '1.0.0'),
            ('CAEC-2024-0002', 'Sistema Demo 2', 'disponible', 'CAEC-V1', '1.0.0'),
            ('CAEC-2024-0003', 'Sistema Demo 3', 'disponible', 'CAEC-V2', '1.2.0'),
            ('CAEC-2024-TEST', 'Sistema Test', 'disponible', 'CAEC-V1', '1.0.0')
        ''')

    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente")

def crear_usuario(nombre, apellido, email, password):
    """Crear un nuevo usuario"""
    conn = get_db_connection()
    cursor = get_cursor(conn)

    # Usar placeholders según el tipo de BD
    placeholder = '%s' if is_postgres() else '?'

    try:
        if is_postgres():
            cursor.execute(f'''
                INSERT INTO usuario (nombre, apellido, email, password)
                VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder})
                RETURNING id
            ''', (nombre, apellido, email, password))
            usuario_id = cursor.fetchone()['id']

            cursor.execute(f'''
                INSERT INTO contacto (usuario_id)
                VALUES ({placeholder})
            ''', (usuario_id,))
        else:
            cursor.execute(f'''
                INSERT INTO usuario (nombre, apellido, email, password)
                VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder})
            ''', (nombre, apellido, email, password))
            usuario_id = cursor.lastrowid

            cursor.execute(f'''
                INSERT INTO contacto (usuario_id)
                VALUES ({placeholder})
            ''', (usuario_id,))

        conn.commit()
        return usuario_id
    except (sqlite3.IntegrityError, psycopg2.IntegrityError):
        return None
    finally:
        conn.close()

def verificar_usuario(email, password):
    """Verificar credenciales de usuario"""
    conn = get_db_connection()
    cursor = get_cursor(conn)
    placeholder = '%s' if is_postgres() else '?'

    # Para PostgreSQL, activo es booleano; para SQLite es 1
    activo_value = True if is_postgres() else 1

    cursor.execute(f'''
        SELECT * FROM usuario
        WHERE email = {placeholder} AND password = {placeholder} AND activo = {placeholder}
    ''', (email, password, activo_value))

    usuario = cursor.fetchone()

    if usuario:
        # Actualizar último acceso
        cursor.execute(f'''
            UPDATE usuario
            SET ultimo_acceso = CURRENT_TIMESTAMP
            WHERE id = {placeholder}
        ''', (usuario['id'],))
        conn.commit()

    conn.close()
    return dict(usuario) if usuario else None

def obtener_sistema_usuario(usuario_id):
    """Obtener el sistema CAEC asociado a un usuario"""
    conn = get_db_connection()
    cursor = get_cursor(conn)
    placeholder = '%s' if is_postgres() else '?'

    cursor.execute(f'''
        SELECT * FROM sistema_caec
        WHERE usuario_id = {placeholder} AND estado = 'activo'
    ''', (usuario_id,))

    sistema = cursor.fetchone()
    conn.close()

    return dict(sistema) if sistema else None

def validar_codigo_sistema(codigo_sistema):
    """Validar si un código de sistema existe y está disponible"""
    conn = get_db_connection()
    cursor = get_cursor(conn)
    placeholder = '%s' if is_postgres() else '?'

    cursor.execute(f'''
        SELECT * FROM sistema_caec
        WHERE codigo_sistema = {placeholder} AND (usuario_id IS NULL OR estado = 'disponible')
    ''', (codigo_sistema,))

    sistema = cursor.fetchone()
    conn.close()

    return dict(sistema) if sistema else None

def vincular_sistema_usuario(codigo_sistema, usuario_id, nombre_sistema=None):
    """Vincular un sistema CAEC a un usuario"""
    conn = get_db_connection()
    cursor = get_cursor(conn)
    placeholder = '%s' if is_postgres() else '?'

    try:
        if nombre_sistema is None:
            nombre_sistema = f"Mi Sistema CAEC"

        cursor.execute(f'''
            UPDATE sistema_caec
            SET usuario_id = {placeholder},
                nombre_sistema = {placeholder},
                fecha_vinculacion = CURRENT_TIMESTAMP,
                ultimo_sync = CURRENT_TIMESTAMP,
                estado = 'activo'
            WHERE codigo_sistema = {placeholder}
        ''', (usuario_id, nombre_sistema, codigo_sistema))

        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    except Exception as e:
        print(f"Error al vincular sistema: {e}")
        conn.close()
        return False

def actualizar_ultimo_sync(sistema_id):
    """Actualizar la última sincronización del sistema"""
    conn = get_db_connection()
    cursor = get_cursor(conn)
    placeholder = '%s' if is_postgres() else '?'

    cursor.execute(f'''
        UPDATE sistema_caec
        SET ultimo_sync = CURRENT_TIMESTAMP
        WHERE id = {placeholder}
    ''', (sistema_id,))

    conn.commit()
    conn.close()

def obtener_usuario_por_id(usuario_id):
    """Obtener datos completos del usuario incluyendo información de contacto"""
    conn = get_db_connection()
    cursor = get_cursor(conn)
    placeholder = '%s' if is_postgres() else '?'

    cursor.execute(f'''
        SELECT u.*, c.telefono, c.celular, c.direccion, c.ciudad, c.pais, c.codigo_postal
        FROM usuario u
        LEFT JOIN contacto c ON u.id = c.usuario_id
        WHERE u.id = {placeholder}
    ''', (usuario_id,))

    usuario = cursor.fetchone()
    conn.close()

    return dict(usuario) if usuario else None

def actualizar_usuario(usuario_id, nombre, apellido, telefono, celular, direccion, ciudad, codigo_postal, pais):
    """Actualizar información del usuario y contacto"""
    conn = get_db_connection()
    cursor = get_cursor(conn)
    placeholder = '%s' if is_postgres() else '?'

    try:
        # Actualizar datos del usuario
        cursor.execute(f'''
            UPDATE usuario
            SET nombre = {placeholder}, apellido = {placeholder}
            WHERE id = {placeholder}
        ''', (nombre, apellido, usuario_id))

        # Actualizar datos de contacto
        cursor.execute(f'''
            UPDATE contacto
            SET telefono = {placeholder}, celular = {placeholder}, direccion = {placeholder},
                ciudad = {placeholder}, codigo_postal = {placeholder}, pais = {placeholder}
            WHERE usuario_id = {placeholder}
        ''', (telefono, celular, direccion, ciudad, codigo_postal, pais, usuario_id))

        conn.commit()
        success = True
    except Exception as e:
        print(f"Error al actualizar usuario: {e}")
        success = False
    finally:
        conn.close()

    return success

def cambiar_password(usuario_id, nueva_password):
    """Cambiar la contraseña del usuario"""
    conn = get_db_connection()
    cursor = get_cursor(conn)
    placeholder = '%s' if is_postgres() else '?'

    try:
        cursor.execute(f'''
            UPDATE usuario
            SET password = {placeholder}
            WHERE id = {placeholder}
        ''', (nueva_password, usuario_id))

        conn.commit()
        success = cursor.rowcount > 0
    except Exception as e:
        print(f"Error al cambiar contraseña: {e}")
        success = False
    finally:
        conn.close()

    return success

def obtener_sistema_activo(usuario_id):
    """Obtener el sistema activo del usuario"""
    conn = get_db_connection()
    cursor = get_cursor(conn)
    placeholder = '%s' if is_postgres() else '?'

    cursor.execute(f'''
        SELECT * FROM sistema_caec
        WHERE usuario_id = {placeholder} AND estado = 'activo'
        LIMIT 1
    ''', (usuario_id,))

    sistema = cursor.fetchone()
    conn.close()

    return dict(sistema) if sistema else None

def obtener_todos_sistemas_usuario(usuario_id, exclude_active=False):
    """Obtener todos los sistemas del usuario"""
    conn = get_db_connection()
    cursor = get_cursor(conn)
    placeholder = '%s' if is_postgres() else '?'

    if exclude_active:
        cursor.execute(f'''
            SELECT * FROM sistema_caec
            WHERE usuario_id = {placeholder} AND estado != 'activo'
            ORDER BY fecha_vinculacion DESC
        ''', (usuario_id,))
    else:
        cursor.execute(f'''
            SELECT * FROM sistema_caec
            WHERE usuario_id = {placeholder}
            ORDER BY fecha_vinculacion DESC
        ''', (usuario_id,))

    sistemas = cursor.fetchall()
    conn.close()

    return [dict(sistema) for sistema in sistemas]

def crear_sistema_caec(usuario_id, nombre, ubicacion, tipo_sistema, descripcion=None):
    """Crear un nuevo sistema CAEC para el usuario"""
    conn = get_db_connection()
    cursor = get_cursor(conn)
    placeholder = '%s' if is_postgres() else '?'

    try:
        # Generar código único para el sistema
        codigo_sistema = f"CAEC-{secrets.token_hex(4).upper()}"

        if is_postgres():
            cursor.execute(f'''
                INSERT INTO sistema_caec
                (codigo_sistema, usuario_id, nombre_sistema, fecha_vinculacion, ultimo_sync, estado, modelo, version_firmware)
                VALUES ({placeholder}, {placeholder}, {placeholder}, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'activo', {placeholder}, '1.0.0')
                RETURNING id
            ''', (codigo_sistema, usuario_id, f"{nombre} ({ubicacion})", tipo_sistema))
            system_id = cursor.fetchone()['id']
        else:
            cursor.execute(f'''
                INSERT INTO sistema_caec
                (codigo_sistema, usuario_id, nombre_sistema, fecha_vinculacion, ultimo_sync, estado, modelo, version_firmware)
                VALUES ({placeholder}, {placeholder}, {placeholder}, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'activo', {placeholder}, '1.0.0')
            ''', (codigo_sistema, usuario_id, f"{nombre} ({ubicacion})", tipo_sistema))
            system_id = cursor.lastrowid

        conn.commit()
        return system_id
    except Exception as e:
        print(f"Error al crear sistema: {e}")
        return None
    finally:
        conn.close()

def activar_sistema(usuario_id, system_id):
    """Activar un sistema específico y desactivar los demás"""
    conn = get_db_connection()
    cursor = get_cursor(conn)
    placeholder = '%s' if is_postgres() else '?'

    try:
        # Desactivar todos los sistemas del usuario
        cursor.execute(f'''
            UPDATE sistema_caec
            SET estado = 'inactivo'
            WHERE usuario_id = {placeholder}
        ''', (usuario_id,))

        # Activar el sistema seleccionado
        cursor.execute(f'''
            UPDATE sistema_caec
            SET estado = 'activo'
            WHERE id = {placeholder} AND usuario_id = {placeholder}
        ''', (system_id, usuario_id))

        conn.commit()
        success = cursor.rowcount > 0
    except Exception as e:
        print(f"Error al activar sistema: {e}")
        success = False
    finally:
        conn.close()

    return success

def eliminar_sistema(usuario_id, system_id):
    """Eliminar un sistema del usuario"""
    conn = get_db_connection()
    cursor = get_cursor(conn)
    placeholder = '%s' if is_postgres() else '?'

    try:
        cursor.execute(f'''
            DELETE FROM sistema_caec
            WHERE id = {placeholder} AND usuario_id = {placeholder}
        ''', (system_id, usuario_id))

        conn.commit()
        success = cursor.rowcount > 0
    except Exception as e:
        print(f"Error al eliminar sistema: {e}")
        success = False
    finally:
        conn.close()

    return success

# Inicializar la base de datos al importar el módulo
if __name__ == "__main__":
    init_db()
