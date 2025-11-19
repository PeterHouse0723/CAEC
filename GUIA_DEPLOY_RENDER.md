# Guía para Desplegar CAEC en Render

Esta guía te ayudará a desplegar tu aplicación CAEC en Render de manera sencilla.

## Preparación Completada ✓

Tu proyecto ya está listo para desplegarse en Render con los siguientes archivos configurados:
- `requirements.txt` - Dependencias de Python (incluyendo Gunicorn)
- `render.yaml` - Configuración de despliegue
- `app.py` - Configurado para producción
- `.gitignore` - Actualizado

## Pasos para Desplegar en Render

### 1. Preparar el Repositorio Git

Primero, asegúrate de que todos los cambios estén en Git:

```bash
git add .
git commit -m "Preparar para despliegue en Render"
git push origin main
```

**IMPORTANTE:** Si aún no has subido tu código a GitHub/GitLab:
1. Crea un nuevo repositorio en GitHub (https://github.com/new)
2. Copia la URL del repositorio
3. Ejecuta:
   ```bash
   git remote add origin <URL-de-tu-repositorio>
   git branch -M main
   git push -u origin main
   ```

### 2. Crear Cuenta en Render

1. Ve a [https://render.com](https://render.com)
2. Haz clic en "Get Started for Free"
3. Regístrate con GitHub (recomendado) o con email

### 3. Conectar tu Repositorio

1. En el dashboard de Render, haz clic en **"New +"**
2. Selecciona **"Web Service"**
3. Conecta tu cuenta de GitHub/GitLab si aún no lo has hecho
4. Busca y selecciona tu repositorio **CAEC**

### 4. Configurar el Web Service

Render detectará automáticamente el archivo `render.yaml`, pero verifica la configuración:

**Configuración Básica:**
- **Name:** `caec-app` (o el nombre que prefieras)
- **Region:** Elige la más cercana a ti
- **Branch:** `main` (o tu rama principal)
- **Runtime:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

**Variables de Entorno:**
Render generará automáticamente `SECRET_KEY`, pero puedes agregar otras si las necesitas:
- `FLASK_ENV` = `production`
- `PYTHON_VERSION` = `3.11.0`

### 5. Seleccionar Plan

- Elige el plan **Free** para empezar (0 USD/mes)
- El plan gratuito incluye:
  - 750 horas de tiempo de ejecución al mes
  - La app se "duerme" después de 15 minutos de inactividad
  - Puede tardar 30-50 segundos en "despertar"

### 6. Desplegar

1. Haz clic en **"Create Web Service"**
2. Render comenzará a construir y desplegar tu aplicación
3. Puedes ver los logs en tiempo real
4. Espera a que aparezca "Live" (generalmente 2-5 minutos)

### 7. Acceder a tu Aplicación

Una vez desplegada, Render te dará una URL como:
```
https://caec-app.onrender.com
```

¡Tu aplicación estará en línea y accesible desde cualquier parte del mundo!

## Consideraciones Importantes

### Base de Datos SQLite

Tu aplicación usa SQLite, que funciona pero tiene limitaciones en producción:

**Limitación:** Los datos se perderán cada vez que Render reinicie el servicio (cada 24-48 horas en plan gratuito).

**Soluciones:**

1. **Para pruebas/desarrollo:** Está bien usar SQLite
2. **Para producción:** Migrar a PostgreSQL
   - Render ofrece PostgreSQL gratuito
   - Necesitarás modificar `database.py` para usar PostgreSQL

### Monitoreo

- **Logs:** Ve a tu servicio en Render > pestaña "Logs"
- **Métricas:** Pestaña "Metrics" para ver uso de CPU/Memoria
- **Alertas:** Configura notificaciones por email

## Actualizaciones Automáticas

Con la configuración actual (`autoDeploy: true`):
- Cada vez que hagas `git push` a la rama `main`
- Render automáticamente desplegará los cambios
- No necesitas hacer nada más

## Dominios Personalizados

Si quieres usar tu propio dominio:
1. Ve a tu servicio > Settings > Custom Domains
2. Agrega tu dominio
3. Configura los registros DNS según las instrucciones

## Solución de Problemas

### La aplicación no inicia

1. Revisa los logs en Render
2. Verifica que `requirements.txt` tenga todas las dependencias
3. Asegúrate de que `gunicorn app:app` sea el comando correcto

### Error 503 Service Unavailable

- La app puede estar "despertando" (plan gratuito)
- Espera 30-50 segundos y recarga

### Errores de Base de Datos

- SQLite se reinicia con cada deploy
- Los datos se perderán periódicamente
- Considera migrar a PostgreSQL para persistencia

## Migración a PostgreSQL (Opcional pero Recomendada)

Para datos persistentes:

1. En Render, crea una base de datos PostgreSQL (plan gratuito disponible)
2. Agrega a `requirements.txt`:
   ```
   psycopg2-binary==2.9.9
   ```
3. Modifica `database.py` para usar PostgreSQL en lugar de SQLite
4. Agrega la variable de entorno `DATABASE_URL` en Render

## Recursos Adicionales

- [Documentación de Render](https://render.com/docs)
- [Guía de Flask en Render](https://render.com/docs/deploy-flask)
- [Precios de Render](https://render.com/pricing)

## Soporte

Si tienes problemas:
1. Revisa los logs en Render
2. Consulta la documentación de Render
3. Verifica que todos los archivos de configuración estén correctos

---

¡Felicidades! Tu aplicación CAEC ahora está en la nube. 🚀
