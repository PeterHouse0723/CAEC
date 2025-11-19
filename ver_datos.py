#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para ver los datos almacenados en la base de datos CAEC
"""

import sqlite3
from datetime import datetime

def ver_base_datos():
    try:
        conn = sqlite3.connect('caec.db')
        cursor = conn.cursor()

        print("\n" + "="*60)
        print("           SISTEMA CAEC - DATOS DE LA BASE DE DATOS")
        print("="*60)

        # USUARIOS REGISTRADOS
        print("\n>>> USUARIOS REGISTRADOS:")
        print("-" * 60)
        cursor.execute("SELECT id, nombre, apellido, email, fecha_registro, activo FROM usuario")
        usuarios = cursor.fetchall()

        if usuarios:
            for row in usuarios:
                print(f"\nID: {row[0]}")
                print(f"  Nombre: {row[1]} {row[2]}")
                print(f"  Email: {row[3]}")
                print(f"  Registrado: {row[4]}")
                print(f"  Estado: {'Activo' if row[5] else 'Inactivo'}")
        else:
            print("  No hay usuarios registrados")

        # SISTEMAS CAEC
        print("\n" + "="*60)
        print(">>> SISTEMAS CAEC:")
        print("-" * 60)
        cursor.execute("""
            SELECT s.id, s.codigo_sistema, s.usuario_id, u.nombre, u.apellido,
                   s.fecha_vinculacion, s.estado, s.modelo
            FROM sistema_caec s
            LEFT JOIN usuario u ON s.usuario_id = u.id
            ORDER BY s.id
        """)
        sistemas = cursor.fetchall()

        if sistemas:
            for row in sistemas:
                print(f"\nSistema: {row[1]} (ID: {row[0]})")
                print(f"  Modelo: {row[7]}")
                if row[2]:  # Tiene usuario vinculado
                    print(f"  Usuario: {row[3]} {row[4]} (ID: {row[2]})")
                    print(f"  Fecha vinculacion: {row[5]}")
                else:
                    print(f"  Estado: DISPONIBLE - Sin vincular")
                print(f"  Estado: {row[6]}")
        else:
            print("  No hay sistemas registrados")

        # INFORMACIÓN DE CONTACTO
        print("\n" + "="*60)
        print(">>> INFORMACION DE CONTACTO:")
        print("-" * 60)
        cursor.execute("""
            SELECT c.id, u.nombre, u.apellido, c.telefono, c.celular,
                   c.direccion, c.ciudad, c.pais
            FROM contacto c
            INNER JOIN usuario u ON c.usuario_id = u.id
        """)
        contactos = cursor.fetchall()

        if contactos:
            for row in contactos:
                print(f"\n{row[1]} {row[2]}:")
                if row[3]:
                    print(f"  Telefono: {row[3]}")
                if row[4]:
                    print(f"  Celular: {row[4]}")
                if row[5]:
                    print(f"  Direccion: {row[5]}")
                if row[6]:
                    print(f"  Ciudad: {row[6]}")
                if row[7]:
                    print(f"  Pais: {row[7]}")
                if not any([row[3], row[4], row[5], row[6], row[7]]):
                    print("  Sin informacion de contacto")
        else:
            print("  No hay informacion de contacto")

        # ESTADÍSTICAS
        print("\n" + "="*60)
        print(">>> ESTADISTICAS:")
        print("-" * 60)

        cursor.execute("SELECT COUNT(*) FROM usuario WHERE activo = 1")
        usuarios_activos = cursor.fetchone()[0]
        print(f"  Usuarios activos: {usuarios_activos}")

        cursor.execute("SELECT COUNT(*) FROM sistema_caec WHERE usuario_id IS NOT NULL")
        sistemas_vinculados = cursor.fetchone()[0]
        print(f"  Sistemas vinculados: {sistemas_vinculados}")

        cursor.execute("SELECT COUNT(*) FROM sistema_caec WHERE usuario_id IS NULL")
        sistemas_disponibles = cursor.fetchone()[0]
        print(f"  Sistemas disponibles: {sistemas_disponibles}")

        print("\n" + "="*60 + "\n")

        conn.close()

    except sqlite3.Error as e:
        print(f"\nError al acceder a la base de datos: {e}")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    ver_base_datos()
