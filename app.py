import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

#cargar las variables de entorno 
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Alumno(db.Model):
    __tablename__ = 'alumnos'
    no_control = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String)
    ap_paterno = db.Column(db.String)
    ap_materno = db.Column(db.String)
    semestre = db.Column(db.Integer)

@app.route('/alumnos', methods=['GET'])
def get_alumnos():
    alumnos = Alumno.query.all()
    lista_alumnos = []
    for alumno in alumnos:
        lista_alumnos.append({
        'no_control': alumno.no_control,
        'nombre': alumno.nombre,
        'ap_paterno': alumno.ap_paterno,
        'ap_materno': alumno.ap_materno,
        'semestre': alumno.semestre
    })
    return jsonify(lista_alumnos)

@app.route('/alumnos', methods=['POST'])
def agregar_alumno():
    data = request.get_json()
    nuevo_alumno = Alumno(
        no_control=data['no_control'],
        nombre=data['nombre'],
        ap_paterno=data['ap_paterno'],
        ap_materno=data['ap_materno'],
        semestre=data['semestre']
    )
    db.session.add(nuevo_alumno)
    db.session.commit()
    return jsonify({'mensaje': 'Alumno agregado exitosamente'}), 201

# Endpoint para obtener un estudiante por no_control
@app.route('/alumnos/<no_control>', methods=['GET'])
def obtener_alumno(no_control):
    alumno = Alumno.query.get(no_control)
    if alumno is None:
        return jsonify({'mensaje': 'Estudiante no encontrado'}), 404
    return jsonify({
        'no_control': alumno.no_control,
        'nombre': alumno.nombre,
        'ap_paterno': alumno.ap_paterno,
        'ap_materno': alumno.ap_materno,
        'semestre': alumno.semestre
    })

# Endpoint para eliminar un alumno
@app.route('/alumnos/<no_control>', methods=['DELETE'])
def eliminar_estudiante(no_control):
    alumno = Alumno.query.get(no_control)
    if alumno is None:
        return jsonify({'mensaje': 'alumno no encontrado'}), 404
    db.session.delete(alumno)
    db.session.commit()
    return jsonify({'mensaje': 'alumno eliminado exitosamente'})

# Endpoint para actualizar un estudiante
@app.route('/alumnos/<no_control>', methods=['PATCH'])
def actualizar_alumno(no_control):
    alumno = Alumno.query.get(no_control)
    if alumno is None:
        return jsonify({'mensaje': 'Alumno no encontrado'}), 404
    data = request.get_json()

    if "nombre" in data:
        alumno.nombre = data['nombre']
    if "ap_paterno" in data:
        alumno.ap_paterno = data['ap_paterno']
    if "ap_materno" in data:
        alumno.ap_materno = data['ap_materno']
    if "semestre" in data:
        alumno.semestre = data['semestre']
    db.session.commit()
    return jsonify({'mensaje': 'Alumno actualizado exitosamente'})

if __name__ == '__main__':
    app.run(debug=True)