import mysql.connector

database = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password='',
    database='eventos'
)

def registrar_usuario(nombre, correo, clave, foto_perfil, rol_id):
    cursor = database.cursor()
    insert_query = "INSERT INTO usuarios (nombre, correo, clave, foto_perfil, rol_id) VALUES (%s, %s, %s, %s, %s)"
    datos_usuario = (nombre, correo, clave, foto_perfil, rol_id)
    cursor.execute(insert_query, datos_usuario)
    database.commit()
    
    # Obtener el usuario_id generado
    usuario_id = cursor.lastrowid
    
    cursor.close()
    return usuario_id


def existe_usuario_por_correo(correo):
    cursor = database.cursor()
    query = "SELECT COUNT(*) FROM usuarios WHERE correo = %s"
    cursor.execute(query, (correo,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count > 0

def iniciar_sesion(correo, clave):
    cursor = database.cursor(dictionary=True)
    query = "SELECT * FROM usuarios WHERE correo = %s AND clave = %s"
    cursor.execute(query, (correo, clave))
    usuario = cursor.fetchone()
    cursor.close()
    return usuario

def obtener_usuario_por_id(usuario_id):
    cursor = database.cursor(dictionary=True)
    query = "SELECT * FROM usuarios WHERE usuario_id = %s"
    cursor.execute(query, (usuario_id,))
    usuario = cursor.fetchone()
    cursor.close()
    return usuario

def editar_perfil(usuario_id, nombre, foto_perfil):
    cursor = database.cursor()
    update_query = "UPDATE usuarios SET nombre = %s, foto_perfil = %s WHERE usuario_id = %s"
    datos_usuario = (nombre, foto_perfil, usuario_id)
    cursor.execute(update_query, datos_usuario)
    database.commit()
    cursor.close()

def crear_evento(titulo, descripcion, fecha, hora, lugar, capacidad_maxima, organizador_id):
    cursor = database.cursor()
    insert_query = "INSERT INTO evento (titulo, descripcion, fecha, hora, lugar, capacidad_maxima, organizador_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    datos_evento = (titulo, descripcion, fecha, hora, lugar, capacidad_maxima, organizador_id)
    cursor.execute(insert_query, datos_evento)
    database.commit()
    cursor.close()

def obtener_evento_por_id(evento_id):
    cursor = database.cursor(dictionary=True)
    query = "SELECT * FROM evento WHERE evento_id = %s"
    cursor.execute(query, (evento_id,))
    evento = cursor.fetchone()
    cursor.close()
    return evento

def obtener_eventos():
    cursor = database.cursor(dictionary=True)
    query = "SELECT * FROM evento"
    cursor.execute(query)
    eventos = cursor.fetchall()
    cursor.close()
    return eventos

def obtener_eventos_usuario(organizador_id):
    cursor = database.cursor(dictionary=True)
    query = "SELECT * FROM evento WHERE organizador_id = %s"
    cursor.execute(query, (organizador_id,))
    eventos = cursor.fetchall()
    cursor.close()
    return eventos

def registrar_en_evento(usuario_id, evento_id):
    cursor = database.cursor()
    insert_query = "INSERT INTO registros_eventos (usuario_id, evento_id) VALUES (%s, %s)"
    datos_registro = (usuario_id, evento_id)
    cursor.execute(insert_query, datos_registro)
    database.commit()
    cursor.close()

def usuario_ya_registrado(usuario_id, evento_id):
    cursor = database.cursor()
    query = "SELECT * FROM registros_eventos WHERE usuario_id = %s AND evento_id = %s"
    cursor.execute(query, (usuario_id, evento_id))
    registro = cursor.fetchone()
    cursor.close()
    return registro is not None

def obtener_registros_de_evento(evento_id):
    cursor = database.cursor(dictionary=True)
    query = "SELECT usuarios.* FROM registros_eventos INNER JOIN usuarios ON registros_eventos.usuario_id = usuarios.usuario_id WHERE registros_eventos.evento_id = %s"
    cursor.execute(query, (evento_id,))
    registros = cursor.fetchall()
    cursor.close()
    return registros

def enviar_notificacion(usuario_id, evento_id, mensaje):
    cursor = database.cursor()
    insert_query = "INSERT INTO notificaciones (usuario_id, evento_id, mensaje) VALUES (%s, %s, %s)"
    datos_notificacion = (usuario_id, evento_id, mensaje)
    cursor.execute(insert_query, datos_notificacion)
    database.commit()
    cursor.close()

def obtener_notificaciones_usuario(usuario_id):
    cursor = database.cursor(dictionary=True)
    query = "SELECT * FROM notificaciones WHERE usuario_id = %s"
    cursor.execute(query, (usuario_id,))
    notificaciones = cursor.fetchall()
    cursor.close()
    return notificaciones

def agregar_usuario_prueba():
    try:
        cursor = database.cursor()
        insert_query = "INSERT INTO usuarios (nombre, correo, clave, rol_id) VALUES (%s, %s, %s, %s)"
        datos_usuario = ('Usuario Prueba', 'prueba@example.com', 'clave123', 1)  # Ejemplo de datos de prueba
        cursor.execute(insert_query, datos_usuario)
        database.commit()
        cursor.close()
        print("Usuario de prueba agregado exitosamente.")
    except mysql.connector.Error as error:
        print(f"Error al agregar usuario de prueba: {error}")
        database.rollback()

def obtener_eventos_disponibles():
    cursor = database.cursor(dictionary=True)
    query = "SELECT * FROM evento WHERE fecha >= CURDATE()"
    cursor.execute(query)
    eventos = cursor.fetchall()
    cursor.close()
    return eventos

def obtener_eventos_filtrados(fecha=None, lugar=None):
    cursor = database.cursor(dictionary=True)
    query = "SELECT * FROM evento WHERE 1=1"  # Consulta base
    params = []
    
    if fecha:
        query += " AND fecha = %s"
        params.append(fecha)
        
    if lugar:
        query += " AND lugar LIKE %s"
        params.append(f"%{lugar}%")
    
    cursor.execute(query, params)
    eventos = cursor.fetchall()
    cursor.close()
    return eventos

def obtener_eventos_registrados_por_usuario(usuario_id):
    cursor = database.cursor(dictionary=True)
    query = """
        SELECT e.* 
        FROM registros_eventos re
        JOIN evento e ON re.evento_id = e.evento_id
        WHERE re.usuario_id = %s
    """
    cursor.execute(query, (usuario_id,))
    eventos = cursor.fetchall()
    for evento in eventos:
        query_registrados = """
            SELECT u.nombre, u.correo
            FROM registros_eventos re
            JOIN usuarios u ON re.usuario_id = u.usuario_id
            WHERE re.evento_id = %s
        """
        cursor.execute(query_registrados, (evento['evento_id'],))
        evento['usuarios_registrados'] = cursor.fetchall()
    cursor.close()
    return eventos

def actualizar_perfil(usuario_id, nombre=None, nueva_contrasena=None, foto_perfil=None):
    cursor = database.cursor()
    
    # Construcción de la consulta SQL
    update_query = "UPDATE usuarios SET"
    datos_usuario = []
    
    if nombre:
        update_query += " nombre = %s,"
        datos_usuario.append(nombre)
    
    if nueva_contrasena:
        update_query += " clave = %s,"
        datos_usuario.append(nueva_contrasena)
    
    if foto_perfil:
        update_query += " foto_perfil = %s,"
        datos_usuario.append(foto_perfil)
    
    # Eliminamos la última coma del query y agregamos la condición WHERE
    if update_query.endswith(','):
        update_query = update_query.rstrip(',')
    
    update_query += " WHERE usuario_id = %s"
    datos_usuario.append(usuario_id)
    
    cursor.execute(update_query, datos_usuario)
    database.commit()
    cursor.close()




# Llamamos a la función para agregar el usuario de prueba si ejecutamos db.py directamente
if __name__ == '__main__':
    agregar_usuario_prueba()
