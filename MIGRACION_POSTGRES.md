# Migración a PostgreSQL para Persistencia de Datos

## Estado Actual

Tu aplicación CAEC ya está **parcialmente preparada** para usar PostgreSQL. Los archivos modificados incluyen:

- ✅ `requirements.txt` - Incluye `psycopg2-binary`
- ✅ `render.yaml` - Configurado para crear base de datos PostgreSQL
- ⚠️ `database.py` - Requiere ajustes adicionales para compatibilidad completa

## Opción 1: Despliegue Rápido (Recomendado para Empezar)

### Usar SQLite Temporalmente

Si quieres desplegar **ahora mismo** y no te import an que los datos se reinicien periódicamente:

1. **Elimina** la sección `databases:` de `render.yaml`
2. **Elimina** la variable `DATABASE_URL` de `render.yaml`
3. Despliega normalmente

**Limitación:** Los datos se perderán cada 24-48 horas cuando Render reinicie el servicio.

### Pasos:
```yaml
# render.yaml simplificado
services:
  - type: web
    name: caec-app
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
    autoDeploy: true
```

## Opción 2: PostgreSQL Completo (Datos Permanentes)

### Paso 1: Finalizar Código de database.py

El archivo `database.py` necesita que **todas** las queries SQL usen placeholders dinámicos.

**Estado actual:** Solo algunas funciones están actualizadas (`crear_usuario`, `verificar_usuario`)

**Funciones que necesitan actualización:**
- `obtener_sistema_usuario`
- `validar_codigo_sistema`
- `vincular_sistema_usuario`
- `actualizar_ultimo_sync`
- `obtener_usuario_por_id`
- `actualizar_usuario`
- `cambiar_password`
- `obtener_sistema_activo`
- `obtener_todos_sistemas_usuario`
- `crear_sistema_caec`
- `activar_sistema`
- `eliminar_sistema`

**Patrón de actualización:**

Antes (SQLite only):
```python
def obtener_sistema_usuario(usuario_id):
    conn = get_db_connection()
    cursor = conn.cursor()  # ❌ Solo SQLite

    cursor.execute('''
        SELECT * FROM sistema_caec
        WHERE usuario_id = ?  # ❌ Solo SQLite
    ''', (usuario_id,))
```

Después (SQLite + PostgreSQL):
```python
def obtener_sistema_usuario(usuario_id):
    conn = get_db_connection()
    cursor = get_cursor(conn)  # ✅ Funciona con ambas
    placeholder = '%s' if is_postgres() else '?'  # ✅ Dinámico

    cursor.execute(f'''
        SELECT * FROM sistema_caec
        WHERE usuario_id = {placeholder}  # ✅ Funciona con ambas
    ''', (usuario_id,))
```

### Paso 2: Desplegar en Render

Una vez actualizadas todas las funciones:

1. Commit y push de cambios:
```bash
git add .
git commit -m "Soporte completo para PostgreSQL"
git push origin main
```

2. En Render, el archivo `render.yaml` automáticamente:
   - Creará una base de datos PostgreSQL gratuita
   - Conectará la app a la base de datos
   - Inicializará las tablas automáticamente

### Paso 3: Verificar

1. Ve a Render Dashboard → Tu servicio → Logs
2. Busca el mensaje: "Base de datos inicializada correctamente"
3. Verifica que puedas registrar usuarios y que los datos persistan

## Opción 3: Solución Híbrida (Desarrollo Local + Producción)

**Ventaja:** Tu código actual **ya soporta esto**

- **Local:** Usa SQLite (`caec.db`) - para desarrollo
- **Producción (Render):** Usa PostgreSQL - datos permanentes

**Cómo funciona:**
```python
# En database.py - YA IMPLEMENTADO
def get_db_connection():
    database_url = os.environ.get('DATABASE_URL')

    if database_url:
        # PostgreSQL en Render
        return psycopg2.connect(database_url)
    else:
        # SQLite en local
        return sqlite3.connect('caec.db')
```

**Solo necesitas:** Actualizar las funciones restantes (ver Opción 2, Paso 1)

## Script de Actualización Automática

Puedes usar este script Python para actualizar database.py automáticamente:

```python
# update_database.py
import re

def update_function(func_content):
    """Actualiza una función para usar placeholders dinámicos"""
    # Si ya tiene placeholder, skip
    if "placeholder = " in func_content:
        return func_content

    # Si no tiene queries con ?, skip
    if "?" not in func_content or "execute" not in func_content:
        return func_content

    # Agregar placeholder después de la definición de cursor
    func_content = re.sub(
        r'(cursor = get_cursor\(conn\))\n',
        r'\1\n    placeholder = \'%s\' if is_postgres() else \'?\'\n',
        func_content
    )

    # Reemplazar ? con {placeholder} en queries
    func_content = re.sub(
        r'WHERE\s+(\w+)\s+=\s+\?',
        r'WHERE \1 = {placeholder}',
        func_content
    )
    func_content = re.sub(
        r'VALUES\s+\(\?',
        r'VALUES ({placeholder}',
        func_content
    )
    func_content = re.sub(
        r'SET\s+(\w+)\s+=\s+\?',
        r'SET \1 = {placeholder}',
        func_content
    )

    # Convertir queries a f-strings
    func_content = re.sub(
        r"(cursor\.execute\(''')",
        r"\1f'''",
        func_content
    )

    return func_content

# Leer archivo
with open('database.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Actualizar
# ... aplicar update_function a cada función ...

print("database.py actualizado")
```

## Recomendación

Para **desplegar hoy**:
- Usa **Opción 1** (SQLite temporal)
- Despliega y prueba que todo funcione
- Luego migra a PostgreSQL (Opción 2) cuando tengas tiempo

Para **datos permanentes desde el inicio**:
- Completa las actualizaciones de `database.py` (Opción 2)
- El `render.yaml` ya está listo
- Despliega directamente con PostgreSQL

## Soporte

Si necesitas ayuda:
1. Revisa los logs en Render Dashboard
2. Verifica que `DATABASE_URL` esté configurada en Variables de Entorno
3. Asegúrate de que todas las funciones usen `get_cursor(conn)` y placeholders dinámicos

---

**Nota:** La configuración actual en `render.yaml` ya está lista para PostgreSQL. Solo falta completar las actualizaciones en `database.py`.
