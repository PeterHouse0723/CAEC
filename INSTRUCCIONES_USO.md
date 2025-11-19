# Sistema CAEC - Instrucciones de Uso

## 🚀 Inicio Rápido

La aplicación está corriendo en: **http://127.0.0.1:5000**

## 📋 Flujo de Usuario

### 1. Página de Inicio (Index)
- Accede a `http://127.0.0.1:5000/`
- Página de bienvenida del sistema CAEC

### 2. Login
- Haz clic en el botón de login o accede a `http://127.0.0.1:5000/login`
- Ingresa cualquier email y contraseña (se creará un usuario automáticamente)
- **Ejemplo**:
  - Email: `usuario@test.com`
  - Contraseña: `1234`

### 3. Añadir Sistema CAEC
**Esta página solo aparece si el usuario NO tiene un sistema CAEC vinculado**

- Se te redirigirá automáticamente a la página de añadir sistema
- Puedes elegir entre dos métodos:
  - **Código Manual**: Ingresa el código del sistema
  - **Escanear QR**: (En desarrollo)

#### Códigos de Prueba Disponibles:
```
CAEC-2024-0001
CAEC-2024-0002
CAEC-2024-0003
CAEC-2024-TEST
```

- Ingresa uno de los códigos anteriores
- Haz clic en "Validar Sistema"
- Verás una animación de sincronización con 5 pasos:
  1. Validando código del sistema
  2. Conectando con el sistema
  3. Sincronizando sensores
  4. Configurando parámetros
  5. Finalizando configuración

### 4. Panel de Control (Dashboard)
- Una vez vinculado el sistema, serás redirigido automáticamente al dashboard
- Si cierras sesión y vuelves a entrar, irás directamente aquí (ya no verás la página de añadir sistema)

## 🗄️ Base de Datos

La aplicación crea automáticamente un archivo `caec.db` con las siguientes tablas:

### Tabla `usuario`
- id, nombre, apellido, email, password
- fecha_registro, ultimo_acceso, activo

### Tabla `contacto`
- id, usuario_id, telefono, celular
- direccion, ciudad, pais, codigo_postal

### Tabla `sistema_caec`
- id, codigo_sistema, usuario_id
- nombre_sistema, fecha_vinculacion, ultimo_sync
- estado, modelo, version_firmware

### Tabla `sensor_data` (histórico)
- id, sistema_id, timestamp
- nivel_agua, ph, temperatura, nivel_nutrientes
- irrigacion_activa, luz_activa

## 🔄 Flujo Completo

```
Index → Login → ¿Tiene Sistema?
                     ↓ NO           ↓ SÍ
              Añadir Sistema → Dashboard
                     ↓
              Sincronización
                     ↓
                 Dashboard
```

## ⚙️ Control de Irrigación

En el dashboard, haz clic en la tarjeta de **Irrigación** para acceder a:

### Modo de Ahorro de Energía
- **Barra deslizante**: Ajusta la potencia de la bomba (0-100%)
- **Duración**: Configura cuántos minutos durará el modo ahorro

### Irrigación Abundante
- **Duración**: Configura cuántos minutos la bomba funcionará al 100%
- Después del periodo abundante, cambia automáticamente al modo ahorro

## 🎨 Características Visuales

- **Tarjetas**: Escala de grises minimalista (blanco y negro)
- **Resumen del Sistema**: Mantiene los colores originales
- **Animaciones**: Olas de agua, gotas, sincronización
- **Responsive**: Se adapta a móviles, tablets y escritorio

## 🔐 Seguridad

- Cada usuario puede tener un solo sistema CAEC vinculado
- Los códigos de sistema son únicos
- Un sistema no puede estar vinculado a múltiples usuarios simultáneamente
- Las sesiones se manejan con Flask sessions

## 🧪 Para Desarrollo

Para reiniciar la base de datos:
```bash
cd "g:\Mi unidad\PETER\U\6\Emprendimiento II\CAEC\CAEC"
python database.py
```

Para iniciar el servidor:
```bash
cd "g:\Mi unidad\PETER\U\6\Emprendimiento II\CAEC\CAEC"
python app.py
```

## 📱 Próximas Funcionalidades

- Escáner QR real con cámara
- Historial de datos de sensores
- Gráficos de tendencias
- Alertas y notificaciones
- Múltiples sistemas por usuario
- Panel de administración
