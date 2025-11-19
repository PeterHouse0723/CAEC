from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from database import (
    init_db, crear_usuario, verificar_usuario, obtener_sistema_usuario,
    validar_codigo_sistema, vincular_sistema_usuario, actualizar_ultimo_sync
)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'caec_secret_key_2024')  # Usa variable de entorno en producción

# Inicializar base de datos al iniciar la aplicación
init_db()

# Ruta para la página de inicio - redirige directamente al login
@app.route('/')
def index():
    return redirect(url_for('login'))

# Ruta para la página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validaciones
        if not all([nombre, apellido, email, password, confirm_password]):
            return render_template('register.html', error='Todos los campos son obligatorios')

        if password != confirm_password:
            return render_template('register.html', error='Las contraseñas no coinciden')

        if len(password) < 4:
            return render_template('register.html', error='La contraseña debe tener al menos 4 caracteres')

        # Crear usuario
        user_id = crear_usuario(nombre, apellido, email, password)

        if user_id:
            # Guardar en sesión
            session['user_id'] = user_id
            session['user_email'] = email
            session['user_name'] = f"{nombre} {apellido}"

            # Redirigir a añadir sistema
            return redirect(url_for('add_system'))
        else:
            return render_template('register.html', error='El correo electrónico ya está registrado')

    return render_template('register.html')

# Ruta para la página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')

        # Validaciones
        if not email or not password:
            return render_template('login.html', error='Por favor ingresa email y contraseña')

        # Verificar credenciales
        usuario = verificar_usuario(email, password)

        if usuario:
            # Guardar información del usuario en sesión
            session['user_id'] = usuario['id']
            session['user_email'] = usuario['email']
            session['user_name'] = f"{usuario['nombre']} {usuario['apellido']}"

            # Verificar si el usuario tiene un sistema CAEC vinculado
            sistema = obtener_sistema_usuario(usuario['id'])

            if sistema:
                # Usuario ya tiene sistema, ir directo al dashboard
                session['sistema_id'] = sistema['id']
                session['sistema_codigo'] = sistema['codigo_sistema']
                return redirect(url_for('inicio'))
            else:
                # Usuario no tiene sistema, mostrar página para añadir
                return redirect(url_for('add_system'))
        else:
            # Credenciales inválidas
            return render_template('login.html', error='Email o contraseña incorrectos')

    return render_template('login.html')

# Ruta para añadir sistema CAEC
@app.route('/add-system')
def add_system():
    # Verificar si el usuario está autenticado
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Si ya tiene sistema, redirigir al dashboard
    sistema = obtener_sistema_usuario(session['user_id'])
    if sistema:
        session['sistema_id'] = sistema['id']
        session['sistema_codigo'] = sistema['codigo_sistema']
        return redirect(url_for('inicio'))

    return render_template('add_system.html')

# Ruta para el dashboard
@app.route('/inicio')
def inicio():
    # Verificar si el usuario está autenticado
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Verificar si tiene sistema vinculado
    if 'sistema_id' not in session:
        sistema = obtener_sistema_usuario(session['user_id'])
        if sistema:
            session['sistema_id'] = sistema['id']
            session['sistema_codigo'] = sistema['codigo_sistema']
        else:
            return redirect(url_for('add_system'))

    return render_template('inicio.html', user_name=session.get('user_name', 'Usuario'))

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# API para obtener datos del sistema (para futuro uso con sensores reales)
@app.route('/api/system-data')
def system_data():
    # Aquí se integrarían los datos reales de los sensores
    data = {
        'waterLevel': 75,
        'phLevel': 6.5,
        'waterTemp': 22,
        'nutrientLevel': 85,
        'irrigationActive': True,
        'lightActive': True,
        'timestamp': 'now'
    }
    return jsonify(data)

# API para actualizar configuración del sistema
@app.route('/api/update-system', methods=['POST'])
def update_system():
    data = request.get_json()
    # Aquí se enviarían los comandos al sistema físico
    return jsonify({'status': 'success', 'message': 'Configuración actualizada'})

# API para actualizar configuración de irrigación
@app.route('/api/update-irrigation-config', methods=['POST'])
def update_irrigation_config():
    data = request.get_json()
    config = data.get('config', {})

    # Aquí se guardaría la configuración en una base de datos
    # y se enviarían los parámetros al controlador del sistema físico
    print(f"Nueva configuración de irrigación:")
    print(f"  - Potencia en modo ahorro: {config.get('savingPower')}%")
    print(f"  - Duración modo ahorro: {config.get('savingDuration')} minutos")
    print(f"  - Duración irrigación abundante: {config.get('abundantDuration')} minutos")

    return jsonify({
        'status': 'success',
        'message': 'Configuración de irrigación guardada',
        'config': config
    })

# API para validar código de sistema
@app.route('/api/validate-system', methods=['POST'])
def validate_system():
    data = request.get_json()
    codigo_sistema = data.get('codigo_sistema', '').strip().upper()

    if not codigo_sistema:
        return jsonify({
            'success': False,
            'message': 'Código de sistema no proporcionado'
        })

    # Validar que el código existe y está disponible
    sistema = validar_codigo_sistema(codigo_sistema)

    if sistema:
        return jsonify({
            'success': True,
            'message': 'Sistema válido',
            'sistema': {
                'codigo': sistema['codigo_sistema'],
                'modelo': sistema['modelo'],
                'version': sistema['version_firmware']
            }
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Código de sistema no válido o ya está en uso'
        })

# API para vincular sistema a usuario
@app.route('/api/link-system', methods=['POST'])
def link_system():
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'message': 'Usuario no autenticado'
        })

    data = request.get_json()
    codigo_sistema = data.get('codigo_sistema', '').strip().upper()

    if not codigo_sistema:
        return jsonify({
            'success': False,
            'message': 'Código de sistema no proporcionado'
        })

    # Vincular el sistema al usuario
    success = vincular_sistema_usuario(codigo_sistema, session['user_id'])

    if success:
        # Obtener el sistema recién vinculado
        sistema = obtener_sistema_usuario(session['user_id'])
        if sistema:
            session['sistema_id'] = sistema['id']
            session['sistema_codigo'] = sistema['codigo_sistema']

        return jsonify({
            'success': True,
            'message': 'Sistema vinculado exitosamente'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Error al vincular el sistema. Puede que ya esté en uso.'
        })

# Ruta para Mi Cuenta
@app.route('/account', methods=['GET', 'POST'])
def account():
    # Verificar si el usuario está autenticado
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Obtener datos del usuario
    from database import obtener_usuario_por_id
    user = obtener_usuario_por_id(session['user_id'])

    if not user:
        return redirect(url_for('login'))

    return render_template('account.html', user=user)

# Ruta para actualizar cuenta
@app.route('/update_account', methods=['POST'])
def update_account():
    # Verificar si el usuario está autenticado
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Obtener datos del formulario
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    telefono = request.form.get('telefono')
    celular = request.form.get('celular')
    direccion = request.form.get('direccion')
    ciudad = request.form.get('ciudad')
    codigo_postal = request.form.get('codigo_postal')
    pais = request.form.get('pais')

    # Actualizar en la base de datos
    from database import actualizar_usuario
    success = actualizar_usuario(
        session['user_id'],
        nombre, apellido, telefono, celular,
        direccion, ciudad, codigo_postal, pais
    )

    # Obtener datos actualizados
    from database import obtener_usuario_por_id
    user = obtener_usuario_por_id(session['user_id'])

    # Actualizar nombre en sesión
    if success:
        session['user_name'] = f"{nombre} {apellido}"
        return render_template('account.html', user=user, success='Información actualizada correctamente')
    else:
        return render_template('account.html', user=user, error='Error al actualizar la información')

# Ruta para Configuración
@app.route('/config', methods=['GET', 'POST'])
def config():
    # Verificar si el usuario está autenticado
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('config.html')

# Ruta para cambiar contraseña
@app.route('/change_password', methods=['POST'])
def change_password():
    # Verificar si el usuario está autenticado
    if 'user_id' not in session:
        return redirect(url_for('login'))

    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    # Validaciones
    if new_password != confirm_password:
        return render_template('config.html', error='Las contraseñas no coinciden')

    if len(new_password) < 8:
        return render_template('config.html', error='La nueva contraseña debe tener al menos 8 caracteres')

    # Verificar contraseña actual
    from database import verificar_usuario, cambiar_password
    usuario = verificar_usuario(session['user_email'], current_password)

    if not usuario:
        return render_template('config.html', error='La contraseña actual es incorrecta')

    # Cambiar contraseña
    success = cambiar_password(session['user_id'], new_password)

    if success:
        return render_template('config.html', success='Contraseña cambiada correctamente')
    else:
        return render_template('config.html', error='Error al cambiar la contraseña')

# Ruta para Sistemas CAEC
@app.route('/systems')
def systems():
    # Verificar si el usuario está autenticado
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Obtener todos los sistemas del usuario
    from database import obtener_todos_sistemas_usuario, obtener_sistema_activo

    active_system = obtener_sistema_activo(session['user_id'])
    other_systems = obtener_todos_sistemas_usuario(session['user_id'], exclude_active=True)

    return render_template('systems.html', active_system=active_system, other_systems=other_systems)

# Ruta para agregar nuevo sistema
@app.route('/add_system', methods=['POST'])
def add_new_system():
    # Verificar si el usuario está autenticado
    if 'user_id' not in session:
        return redirect(url_for('login'))

    nombre = request.form.get('nombre')
    ubicacion = request.form.get('ubicacion')
    tipo_sistema = request.form.get('tipo_sistema')
    descripcion = request.form.get('descripcion')

    # Crear sistema en la base de datos
    from database import crear_sistema_caec
    system_id = crear_sistema_caec(
        session['user_id'], nombre, ubicacion,
        tipo_sistema, descripcion
    )

    if system_id:
        return redirect(url_for('systems'))
    else:
        from database import obtener_todos_sistemas_usuario, obtener_sistema_activo
        active_system = obtener_sistema_activo(session['user_id'])
        other_systems = obtener_todos_sistemas_usuario(session['user_id'], exclude_active=True)
        return render_template('systems.html',
                             active_system=active_system,
                             other_systems=other_systems,
                             error='Error al crear el sistema')

# Ruta para activar sistema
@app.route('/activate_system/<int:system_id>', methods=['POST'])
def activate_system(system_id):
    # Verificar si el usuario está autenticado
    if 'user_id' not in session:
        return redirect(url_for('login'))

    from database import activar_sistema
    success = activar_sistema(session['user_id'], system_id)

    if success:
        # Actualizar sesión
        session['sistema_id'] = system_id

    return redirect(url_for('systems'))

# Ruta para eliminar sistema
@app.route('/delete_system/<int:system_id>', methods=['POST'])
def delete_system(system_id):
    # Verificar si el usuario está autenticado
    if 'user_id' not in session:
        return redirect(url_for('login'))

    from database import eliminar_sistema
    success = eliminar_sistema(session['user_id'], system_id)

    return redirect(url_for('systems'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
