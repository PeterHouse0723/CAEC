# Sistema CAEC - Guía Completa

## 🚀 Aplicación Lista

La aplicación está corriendo en: **http://127.0.0.1:5000**

---

## 📋 Flujo Completo del Sistema

### 1️⃣ **Página de Inicio (Index)**
- URL: `http://127.0.0.1:5000/`
- Página de bienvenida con información del sistema CAEC
- Botón para ir al login

### 2️⃣ **Registro de Nuevos Usuarios**
- URL: `http://127.0.0.1:5000/register`
- **Campos requeridos:**
  - Nombre
  - Apellido
  - Correo electrónico
  - Contraseña (mínimo 4 caracteres)
  - Confirmar contraseña

- **Características:**
  - ✅ Indicador de fortaleza de contraseña
  - ✅ Validación en tiempo real
  - ✅ Verificación de coincidencia de contraseñas
  - ✅ Prevención de correos duplicados
  - ✅ Mensajes de error claros

- **Después del registro:**
  - Se crea automáticamente el usuario en la base de datos
  - Se inicia sesión automáticamente
  - Se redirige a la página de añadir sistema CAEC

### 3️⃣ **Login**
- URL: `http://127.0.0.1:5000/login`
- Ingresa email y contraseña
- Opción "Recordarme" para guardar el email
- **Link:** "¿No tienes cuenta? Regístrate aquí" → lleva a `/register`

- **Flujo después del login:**
  - ✅ **Si el usuario YA tiene un sistema CAEC vinculado** → Va directo al Dashboard
  - ❌ **Si el usuario NO tiene un sistema CAEC** → Va a la página de añadir sistema

### 4️⃣ **Añadir Sistema CAEC**
- URL: `http://127.0.0.1:5000/add-system`
- Solo aparece si el usuario NO tiene un sistema vinculado
- Dos opciones:
  - 🔢 Ingresar código manualmente
  - 📷 Escanear QR (en desarrollo)

#### **Códigos de Prueba:**
```
CAEC-2024-0001
CAEC-2024-0002
CAEC-2024-0003
CAEC-2024-TEST
```

- **Animación de Sincronización (5 pasos):**
  1. ✓ Validando código del sistema
  2. ✓ Conectando con el sistema
  3. ✓ Sincronizando sensores
  4. ✓ Configurando parámetros
  5. ✓ Finalizando configuración

- **Después de añadir el sistema:**
  - Se vincula el sistema al usuario en la base de datos
  - Se redirige al Dashboard

### 5️⃣ **Dashboard (Panel de Control)**
- URL: `http://127.0.0.1:5000/inicio`
- **Requiere:**
  - Usuario autenticado
  - Sistema CAEC vinculado

- **Características:**
  - 📊 Resumen visual del sistema (torre + tanque con animaciones)
  - 📈 6 tarjetas de sensores en escala de grises
  - ⚙️ Control de irrigación avanzado
  - 🌊 Animaciones de agua en tiempo real

---

## 🗄️ Base de Datos SQLite

Archivo: `caec.db` (creado automáticamente)

### Tablas:

#### **1. usuario**
```sql
- id (PRIMARY KEY)
- nombre
- apellido
- email (UNIQUE)
- password
- fecha_registro
- ultimo_acceso
- activo
```

#### **2. contacto**
```sql
- id (PRIMARY KEY)
- usuario_id (FOREIGN KEY)
- telefono
- celular
- direccion
- ciudad
- pais
- codigo_postal
```

#### **3. sistema_caec**
```sql
- id (PRIMARY KEY)
- codigo_sistema (UNIQUE)
- usuario_id (FOREIGN KEY)
- nombre_sistema
- fecha_vinculacion
- ultimo_sync
- estado
- modelo
- version_firmware
```

#### **4. sensor_data** (histórico)
```sql
- id (PRIMARY KEY)
- sistema_id (FOREIGN KEY)
- timestamp
- nivel_agua
- ph
- temperatura
- nivel_nutrientes
- irrigacion_activa
- luz_activa
```

### **Ver datos de la base de datos:**

Puedes usar cualquier visor de SQLite como:
- **DB Browser for SQLite** (https://sqlitebrowser.org/)
- **SQLite Studio** (https://sqlitestudio.pl/)
- O directamente desde Python:

```python
import sqlite3

conn = sqlite3.connect('caec.db')
cursor = conn.cursor()

# Ver todos los usuarios
cursor.execute("SELECT * FROM usuario")
for row in cursor.fetchall():
    print(row)

# Ver sistemas vinculados
cursor.execute("""
    SELECT u.nombre, u.email, s.codigo_sistema, s.fecha_vinculacion
    FROM usuario u
    LEFT JOIN sistema_caec s ON u.id = s.usuario_id
""")
for row in cursor.fetchall():
    print(row)

conn.close()
```

---

## 🔧 Sistema de Irrigación

En el dashboard, haz clic en la tarjeta de **Irrigación** para acceder a:

### **Modo de Ahorro de Energía:**
- 🎚️ **Barra deslizante visual** (0-100%)
- ⏱️ **Duración del modo ahorro** (en minutos)

### **Irrigación Abundante:**
- 💧 **Duración del periodo al 100%** (en minutos)
- Después cambia automáticamente al modo ahorro

### **Visualización:**
- Cuando la irrigación está ACTIVA:
  - 💦 Columna de agua sube por la torre (2 segundos)
  - 💧 Efecto de salpicado en la parte superior
- Todos los cambios se guardan en la base de datos

---

## 📊 Cómo Ver los Datos Guardados

### **Opción 1: DB Browser for SQLite**

1. Descarga e instala: https://sqlitebrowser.org/
2. Abre el archivo `caec.db`
3. Navega por las tablas:
   - **usuario** → Ver todos los usuarios registrados
   - **sistema_caec** → Ver sistemas y sus vínculos
   - **contacto** → Ver información de contacto

### **Opción 2: Script Python**

Crea un archivo `ver_datos.py`:

```python
import sqlite3
from datetime import datetime

conn = sqlite3.connect('caec.db')
cursor = conn.cursor()

print("\n=== USUARIOS REGISTRADOS ===")
cursor.execute("SELECT id, nombre, apellido, email, fecha_registro FROM usuario")
for row in cursor.fetchall():
    print(f"ID: {row[0]} | {row[1]} {row[2]} | Email: {row[3]} | Registrado: {row[4]}")

print("\n=== SISTEMAS CAEC VINCULADOS ===")
cursor.execute("""
    SELECT s.codigo_sistema, u.nombre, u.apellido, s.fecha_vinculacion, s.estado
    FROM sistema_caec s
    LEFT JOIN usuario u ON s.usuario_id = u.id
""")
for row in cursor.fetchall():
    if row[1]:
        print(f"Sistema: {row[0]} | Usuario: {row[1]} {row[2]} | Vinculado: {row[3]} | Estado: {row[4]}")
    else:
        print(f"Sistema: {row[0]} | DISPONIBLE | Estado: {row[4]}")

conn.close()
```

Ejecuta:
```bash
python ver_datos.py
```

---

## 🔐 Seguridad y Validaciones

### **En el Registro:**
- ✅ Email único (no se permiten duplicados)
- ✅ Contraseña mínima de 4 caracteres
- ✅ Confirmación de contraseña
- ✅ Validación de formato de email

### **En el Login:**
- ✅ Verificación de credenciales contra la base de datos
- ✅ Mensajes de error claros
- ✅ Sesiones seguras con Flask

### **En el Sistema CAEC:**
- ✅ Un usuario solo puede tener un sistema vinculado
- ✅ Un sistema no puede estar vinculado a múltiples usuarios
- ✅ Validación de códigos de sistema

---

## 🎯 Ejemplo Completo de Uso

### **Paso 1: Registrarse**
```
1. Ve a http://127.0.0.1:5000/register
2. Completa el formulario:
   - Nombre: Juan
   - Apellido: Pérez
   - Email: juan@ejemplo.com
   - Contraseña: 1234
   - Confirmar: 1234
3. Haz clic en "Crear Cuenta"
```

### **Paso 2: Añadir Sistema**
```
1. Automáticamente te redirige a /add-system
2. Ingresa el código: CAEC-2024-0001
3. Haz clic en "Validar Sistema"
4. Observa la animación de sincronización (5 pasos)
5. Espera a que termine
```

### **Paso 3: Usar el Dashboard**
```
1. Automáticamente te redirige a /inicio
2. Explora las 6 tarjetas de sensores
3. Haz clic en "Irrigación" para configurar:
   - Ajusta la potencia con la barra deslizante
   - Configura duraciones
   - Guarda la configuración
4. Observa las animaciones del sistema
```

### **Paso 4: Cerrar Sesión y Volver a Entrar**
```
1. Cierra sesión (si hay botón) o ve directamente a /login
2. Ingresa las mismas credenciales:
   - Email: juan@ejemplo.com
   - Contraseña: 1234
3. Esta vez irás DIRECTO al dashboard (ya tienes sistema vinculado)
```

---

## 📁 Estructura del Proyecto

```
CAEC/
├── caec.db                 # Base de datos SQLite
├── app.py                  # Aplicación Flask principal
├── database.py             # Funciones de base de datos
├── templates/
│   ├── index.html         # Página de inicio
│   ├── login.html         # Login
│   ├── register.html      # Registro ✨ NUEVO
│   ├── add_system.html    # Añadir sistema CAEC
│   └── inicio.html        # Dashboard
├── static/
│   ├── css/
│   │   ├── styles.css
│   │   ├── login.css
│   │   └── dashboard.css
│   └── js/
│       ├── login.js       # ✅ CORREGIDO
│       └── dashboard.js
└── GUIA_COMPLETA.md       # Este archivo
```

---

## 🐛 Solución de Problemas

### **Problema: "No puedo pasar del login"**
✅ **SOLUCIONADO:** Se corrigió el archivo `login.js` que estaba interceptando el formulario.

### **Problema: "El email ya existe"**
- Cada email solo puede registrarse una vez
- Usa otro email o inicia sesión con el existente

### **Problema: "Código de sistema inválido"**
- Verifica que el código esté correcto (CAEC-2024-XXXX)
- Usa uno de los códigos de prueba listados arriba

### **Problema: "No puedo ver la base de datos"**
- Asegúrate de que el archivo `caec.db` existe
- Usa DB Browser for SQLite o el script Python

---

## 🎉 ¡Todo Listo!

El sistema está completamente funcional con:

✅ Registro de usuarios
✅ Login con validación
✅ Base de datos SQLite
✅ Vinculación de sistemas CAEC
✅ Dashboard con sensores
✅ Control de irrigación avanzado
✅ Animaciones fluidas
✅ Diseño minimalista en escala de grises

**¡Disfruta tu sistema CAEC! 🌱**
