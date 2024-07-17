from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import os
import db

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'yanely052003@gmail.com'
app.config['MAIL_PASSWORD'] = 'klit lkrl yqjc lzjr'
app.config['MAIL_DEFAULT_SENDER'] = 'yanely052003@gmail.com'

mail = Mail(app)
# Configuración para subida de archivos (opcional)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # Esto asume que 'uploads' está en el directorio actual
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/editar_perfil', methods=['GET', 'POST'])
def editar_perfil():
    if 'usuario_id' in session:
        usuario_id = session['usuario_id']
        
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            foto_perfil = request.files.get('foto')
            nueva_contrasena = request.form.get('contrasena')
            
            # Inicializar photo_path como None
            photo_path = None
            if foto_perfil:
                filename = secure_filename(foto_perfil.filename)
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                foto_perfil.save(photo_path)
            
            # Actualizar la base de datos con todos los cambios posibles
            db.actualizar_perfil(usuario_id, nombre=nombre, nueva_contrasena=nueva_contrasena, foto_perfil=photo_path)
            
            # Actualizar la sesión con los nuevos valores
            if nombre:
                session['nombre'] = nombre
                flash('Nombre actualizado correctamente.')
            
            if photo_path:
                session['foto_perfil'] = filename  # Guardar solo el nombre del archivo en la sesión
                flash('Foto de perfil actualizada correctamente.')
            
            if nueva_contrasena:
                flash('Contraseña actualizada correctamente.')
            
            # Actualizar también el correo electrónico en la sesión si se ha cambiado
            usuario = db.obtener_usuario_por_id(usuario_id)
            if usuario:
                session['correo'] = usuario['correo']  # Actualizar el correo en la sesión
            
            return redirect(url_for('editar_perfil'))
        
        usuario = db.obtener_usuario_por_id(usuario_id)
        return render_template('perfil.html', usuario=usuario)
    
    return redirect(url_for('index'))


from flask import flash, redirect, request, session, url_for
import db

@app.route('/registro', methods=['POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        clave = request.form['clave']
        rol_id = int(request.form['rolId'])
        
        # Verificar si el correo ya está registrado
        if db.existe_usuario_por_correo(correo):
            flash('El correo electrónico ya está registrado.')
            return redirect(url_for('index'))  # Redirige a donde quieras en caso de error
        
        # Si el correo no está registrado, procede con el registro
        foto_perfil = None  # Asume que manejas la foto de perfil adecuadamente en otro lugar
        
        try:
            usuario_id = db.registrar_usuario(nombre, correo, clave, foto_perfil, rol_id)
            
            # Establecer en la sesión del usuario
            session['usuario_id'] = usuario_id
            session['nombre'] = nombre
            session['correo'] = correo
            session['rol_id'] = rol_id
            
            flash('Usuario registrado correctamente.')
            return redirect(url_for('index'))
        
        except Exception as e:
            flash(f'Error al registrar usuario: {str(e)}', 'error')
            return redirect(url_for('index'))


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
            session['correo'] = usuario['correo']
            return redirect(url_for('principal'))
        else:
            flash('Credenciales incorrectas. Verifique su correo y contraseña.', 'error')
            return redirect(url_for('index'))


@app.route('/principal')
def principal():
    if 'usuario_id' in session:
        return render_template('principal.html')
    else:
        return redirect(url_for('index'))

@app.route('/crear_evento', methods=['GET', 'POST'])
def crear_evento():
    if request.method == 'POST':
        # Obtener datos del formulario
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']
        hora = request.form['hora']
        lugar = request.form['lugar']
        capacidad = request.form['capacidad']
        
        # Verificar si el usuario está autenticado
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        
        # Obtener el tipo de usuario desde la sesión (suponiendo que guardas el rol_id)
        rol_id = session.get('rol_id')
        
        # Verificar si el usuario es "Asistente" (suponiendo que el rol de Asistente tiene id 2)
        if rol_id == 2:
            flash('Los asistentes no pueden crear eventos.', 'error')
            return redirect(url_for('principal'))
        
        # Obtener el ID del organizador desde la sesión
        organizador_id = session['usuario_id']
        
        # Llamar a la función para crear el evento en la base de datos
        db.crear_evento(titulo, descripcion, fecha, hora, lugar, capacidad, organizador_id)
        
        # Mostrar mensaje de éxito y redirigir a la página principal
        flash('Evento creado exitosamente.')
        return redirect(url_for('principal'))
    
    # Si es un GET request, simplemente renderizar el formulario de creación
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

@app.route('/proximos')
def proximos_eventos():
    fecha = request.args.get('fecha')
    lugar = request.args.get('lugar')
    
    if fecha or lugar:
        eventos = db.obtener_eventos_filtrados(fecha, lugar)
    else:
        eventos = db.obtener_eventos()
    
    return render_template('proximos.html', eventos=eventos)

@app.route('/registrar_evento/<int:evento_id>', methods=['POST'])
def registrar_evento(evento_id):
    if 'usuario_id' in session:
        usuario_id = session['usuario_id']
        evento = db.obtener_evento_por_id(evento_id)
        
        if not evento:
            flash('Evento no encontrado.', 'error')
            return redirect(url_for('proximos_eventos'))
        
        # Verificar si el usuario ya está registrado en el evento
        if db.usuario_ya_registrado(usuario_id, evento_id):
            flash(f'Ya estás registrado en el evento "{evento["titulo"]}".', 'error')
        else:
            try:
                db.registrar_en_evento(usuario_id, evento_id)
                flash(f'Te has registrado en el evento "{evento["titulo"]}" correctamente.', 'success')
                
                # Enviar notificación por correo electrónico
                usuario = db.obtener_usuario_por_id(usuario_id)
                enviar_correo_registro(usuario['correo'], evento['titulo'])
                
            except Exception as e:
                flash(f'Error al registrar en el evento: {str(e)}', 'error')
        
        return redirect(url_for('proximos_eventos'))
    else:
        flash('Debes iniciar sesión para registrarte en un evento.', 'error')
        return redirect(url_for('index'))


    
def enviar_correo_registro(correo_destinatario, titulo_evento):
    msg = Message("Registro en Evento",
                  recipients=[correo_destinatario])
    msg.body = f"Te has registrado exitosamente en el evento: {titulo_evento}"
    
    try:
        mail.send(msg)
        app.logger.info(f'Correo enviado a {correo_destinatario} para el evento {titulo_evento}')
    except Exception as e:
        app.logger.error(f'Error al enviar correo a {correo_destinatario}: {str(e)}')





    
    
@app.route('/eventos_registrados')
def eventos_registrados():
    if 'usuario_id' in session:
        usuario_id = session['usuario_id']
        eventos = db.obtener_eventos_registrados_por_usuario(usuario_id)
        return render_template('evregistrados.html', eventos=eventos)
    else:
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
