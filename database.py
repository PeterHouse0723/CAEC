import sqlite3
from datetime import datetime
import secrets

def get_db_connection():
    """Obtener conexión a la base de datos SQLite"""
    conn = sqlite3.connect('caec.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializar la base de datos con las tablas necesarias"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabla de usuarios
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
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO usuario (nombre, apellido, email, password)
            VALUES (?, ?, ?, ?)
        ''', (nombre, apellido, email, password))

        usuario_id = cursor.lastrowid

        # Crear registro de contacto vacío
        cursor.execute('''
            INSERT INTO contacto (usuario_id)
            VALUES (?)
        ''', (usuario_id,))

        conn.commit()
        return usuario_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def verificar_usuario(email, password):
    """Verificar credenciales de usuario"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM usuario
        WHERE email = ? AND password = ? AND activo = 1
    ''', (email, password))

    usuario = cursor.fetchone()

    if usuario:
        # Actualizar último acceso
        cursor.execute('''
            UPDATE usuario
            SET ultimo_acceso = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (usuario['id'],))
        conn.commit()

    conn.close()
    return dict(usuario) if usuario else None

def obtener_sistema_usuario(usuario_id):
    """Obtener el sistema CAEC asociado a un usuario"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM sistema_caec
        WHERE usuario_id = ? AND estado = 'activo'
    ''', (usuario_id,))

    sistema = cursor.fetchone()
    conn.close()

    return dict(sistema) if sistema else None

def validar_codigo_sistema(codigo_sistema):
    """Validar si un código de sistema existe y está disponible"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM sistema_caec
        WHERE codigo_sistema = ? AND (usuario_id IS NULL OR estado = 'disponible')
    ''', (codigo_sistema,))

    sistema = cursor.fetchone()
    conn.close()

    return dict(sistema) if sistema else None

def vincular_sistema_usuario(codigo_sistema, usuario_id, nombre_sistema=None):
    """Vincular un sistema CAEC a un usuario"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if nombre_sistema is None:
            nombre_sistema = f"Mi Sistema CAEC"

        cursor.execute('''
            UPDATE sistema_caec
            SET usuario_id = ?,
                nombre_sistema = ?,
                fecha_vinculacion = CURRENT_TIMESTAMP,
                ultimo_sync = CURRENT_TIMESTAMP,
                estado = 'activo'
            WHERE codigo_sistema = ?
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
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE sistema_caec
        SET ultimo_sync = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (sistema_id,))

    conn.commit()
    conn.close()

# Inicializar la base de datos al importar el módulo
if __name__ == "__main__":
    init_db()
