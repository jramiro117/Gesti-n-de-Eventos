from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import db

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        clave = request.form['clave']
        rol_id = int(request.form['rolId'])
        db.registrar_usuario(nombre, correo, clave, None, rol_id)
        return redirect(url_for('principal'))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        clave = request.form['clave']
        usuario = db.iniciar_sesion(correo, clave)
        if usuario:
            session['usuario_id'] = usuario['usuario_id']
            session['nombre'] = usuario['nombre']
            session['rol_id'] = usuario['rol_id']
            return redirect(url_for('principal'))
        else:
            return jsonify({'error': 'Credenciales incorrectas'}), 401

@app.route('/principal')
def principal():
    if 'usuario_id' in session:
        return render_template('principal.html')
    else:
        return redirect(url_for('index'))

@app.route('/crear_evento', methods=['GET', 'POST'])
def crear_evento():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']
        hora = request.form['hora']
        lugar = request.form['lugar']
        capacidad = request.form['capacidad']
        if 'usuario_id' in session:
            organizador_id = session['usuario_id']
        else:
            return redirect(url_for('login'))
        db.crear_evento(titulo, descripcion, fecha, hora, lugar, capacidad, organizador_id)
        flash('Evento creado exitosamente.')
        return redirect(url_for('principal'))
    return render_template('crear.html')

@app.route('/mis_eventos')
def mis_eventos():
    if 'usuario_id' in session:
        usuario_id = session['usuario_id']
        eventos = db.obtener_eventos_usuario(usuario_id)
        for evento in eventos:
            evento['usuarios_registrados'] = db.obtener_registros_de_evento(evento['evento_id'])
        return render_template('miseventos.html', eventos=eventos)
    else:
        return redirect(url_for('index'))

@app.route('/proximos_eventos')
def proximos_eventos():
    if 'usuario_id' in session:
        eventos = db.obtener_eventos_disponibles()
        return render_template('proximos.html', eventos=eventos)
    else:
        return redirect(url_for('index'))

@app.route('/registrar_evento/<int:evento_id>', methods=['POST'])
def registrar_evento(evento_id):
    if 'usuario_id' in session:
        usuario_id = session['usuario_id']
        db.registrar_en_evento(usuario_id, evento_id)
        evento = db.obtener_evento_por_id(evento_id)
        if evento:
            nombre_evento = evento['titulo']
            flash(f'Te has registrado en el evento "{nombre_evento}" correctamente.')
        return redirect(url_for('proximos_eventos'))
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
