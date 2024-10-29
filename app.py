from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session

QUERY_TODOS_LOS_ALUMNOS = "SELECT padron, nombre, apellido FROM alumnos"

QUERY_ALUMNO_BY_ID = "SELECT nombre, apellido FROM alumnos WHERE padron = :padron"

QUERY_INGRESAR_ALUMNO = "INSERT INTO alumnos (padron, nombre, apellido) VALUES (:padron, :nombre, :apellido)"

QUERY_ACTUALIZAR_ALUMNO = "UPDATE alumnos SET nombre = :nombre, apellido = :apellido WHERE padron = :padron"

QUERY_BORRAR_ALUMNO = "DELETE FROM alumnos WHERE padron = :padron"

QUERY_NOTA_POR_ALUMNO = """
SELECT nota, nombre, apellido
FROM notas
INNER JOIN alumnos on alumnos.padron = notas.padron 
WHERE nombre = :nombre and apellido = :apellido
"""

# string de conexión a la base de datos: mysql://usuario:password@host:puerto/nombre_schema
engine = create_engine("mysql://root:root@localhost:3306/IDS_API")

Session = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

def all_alumnos():
    conn = Session()
    result = conn.execute(text(QUERY_TODOS_LOS_ALUMNOS)).fetchall()
    conn.close()

    return result

@app.route('/api/v1/alumnos', methods=['GET'])
def get_all_alumnos():
    try:
        result = all_alumnos()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({'padron': row[0], 'nombre': row[1], 'apellido': row[2]})

    return jsonify(response), 200

def alumno_by_id(padron):
    conn = Session()
    result = conn.execute(text(QUERY_ALUMNO_BY_ID), {'padron': padron}).fetchall()
    conn.close()

    return result

@app.route('/api/v1/alumnos/<int:padron>', methods=['GET'])
def get_by_padron(padron):
    try:
        result = alumno_by_id(padron)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    if len(result) == 0:
        return jsonify({'error': 'No se encontró el alumno'}), 404 # Not found

    result = result[0]
    return jsonify({'nombre': result[0], 'apellido': result[1]}), 200


def insert_alumno(data):
    conn = Session()
    conn.execute(text(QUERY_INGRESAR_ALUMNO), params=data)
    conn.commit()
    conn.close()

@app.route('/api/v1/alumnos', methods=['POST'])
def add_alumno():
    data = request.get_json()

    keys = ('padron', 'nombre', 'apellido')
    for key in keys:
        if key not in data:
            return jsonify({'error': f'Faltan el dato {key}'}), 400

    try:
        result = alumno_by_id(data['padron'])
        if len(result) > 0:
            return jsonify({'error': 'El alumno ya existe'}), 400

        insert_alumno(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(data), 201


def actualizar_alumno(padron, data):
    conn = Session()
    conn.execute(text(QUERY_ACTUALIZAR_ALUMNO), params={'padron': padron, **data})
    conn.commit()
    conn.close()
@app.route('/api/v1/alumnos/<int:padron>', methods=['PUT'])
def update_alumno(padron):
    data = request.get_json()

    keys = ('nombre', 'apellido')
    for key in keys:
        if key not in data:
            return jsonify({'error': f'Falta el dato {key}'}), 400

    try:
        result = alumno_by_id(padron)
        if len(result) == 0:
            return jsonify({'error': 'No se encontró el alumno'}), 404

        actualizar_alumno(padron, data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'padron': padron, **data}), 200

def borra_alumno(padron):
    conn = Session()
    conn.execute(text(QUERY_BORRAR_ALUMNO), {'padron': padron})
    conn.commit()
    conn.close()

@app.route('/api/v1/alumnos/<int:padron>', methods=['DELETE'])
def delete_alumno(padron):
    try:
        result = alumno_by_id(padron)
        if len(result) == 0:
            return jsonify({'error': 'No se encontró el alumno'}), 404

        borra_alumno(padron)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    result = result[0]
    return jsonify({'nombre': result[0], 'apellido': result[1], 'padron': padron}), 200

def buscar_alumnos(argumentos):
    query = QUERY_TODOS_LOS_ALUMNOS

    """"
    Si estan mas cancheros con esto, pueden hacerlo asi:
    query_filtros = " AND ".join([f"{key} = :{key}" for key, value in argumentos.items()])
    query_filtros = f" WHERE {query_filtros}" if len(query_filtros) > 0 else ""
    """

    parametros = {}
    query_filtros = ""
    for filtro in argumentos.keys():
        if filtro in request.args:
            if len(query_filtros) > 0:
                query_filtros += " AND "
            query_filtros += f"{filtro} = :{filtro}"
            parametros[filtro] = request.args[filtro]

    if len(query_filtros) > 0:
        query += f" WHERE {query_filtros}"

    conn = Session()
    result = conn.execute(text(query), parametros).fetchall()
    conn.close()

    return result


@app.route('/api/v1/alumnos/search', methods=['GET'])
def search_alumnos():
    try:
        result = buscar_alumnos(request.args)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({'padron': row[0], 'nombre': row[1], 'apellido': row[2]})

    return jsonify(response), 200


def notas_by_alumno(nombre, apellido):
    conn = Session()
    result = conn.execute(text(QUERY_NOTA_POR_ALUMNO), {'nombre': nombre, 'apellido': apellido}).fetchall()
    conn.close()

    return result

@app.route('/api/v1/notas/<string:nombre>/<string:apellido>', methods=['GET'])
def get_notas_by_alumno(nombre, apellido):
    try:
        result = notas_by_alumno(nombre, apellido)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({'nota': row[0], 'nombre': row[1], 'apellido': row[2]})

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
