from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os

app = Flask(__name__)
app.secret_key = 'caec_secret_key_2024'  # Cambiar en producción

# Ruta para la página de inicio/bienvenida
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para la página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')

        # Aquí puedes agregar la lógica de autenticación
        # Por ahora, aceptamos cualquier login
        session['user'] = email
        return redirect(url_for('inicio'))

    return render_template('login.html')

# Ruta para el dashboard
@app.route('/inicio')
def inicio():
    # Verificar si el usuario está autenticado (opcional)
    # if 'user' not in session:
    #     return redirect(url_for('login'))

    return render_template('inicio.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user', None)
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

if __name__ == '__main__':
    app.run(debug=True)
