from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from database import (
    init_db, crear_usuario, verificar_usuario, obtener_sistema_usuario,
    validar_codigo_sistema, vincular_sistema_usuario, actualizar_ultimo_sync
)

app = Flask(__name__)
app.secret_key = 'caec_secret_key_2024'  # Cambiar en producción

# Inicializar base de datos al iniciar la aplicación
init_db()

# Ruta para la página de inicio/bienvenida
@app.route('/')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(debug=True)
