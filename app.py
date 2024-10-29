from flask import Flask, jsonify, request

import alumnos

app = Flask(__name__)

@app.route('/api/v1/alumnos', methods=['GET'])
def get_all_alumnos():
    try:
        result = alumnos.all_alumnos()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({'padron': row[0], 'nombre': row[1], 'apellido': row[2]})

    return jsonify(response), 200


@app.route('/api/v1/alumnos/<int:padron>', methods=['GET'])
def get_by_padron(padron):
    try:
        result = alumnos.alumno_by_id(padron)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    if len(result) == 0:
        return jsonify({'error': 'No se encontró el alumno'}), 404 # Not found

    result = result[0]
    return jsonify({'nombre': result[0], 'apellido': result[1]}), 200


@app.route('/api/v1/alumnos', methods=['POST'])
def add_alumno():
    data = request.get_json()

    keys = ('padron', 'nombre', 'apellido')
    for key in keys:
        if key not in data:
            return jsonify({'error': f'Faltan el dato {key}'}), 400

    try:
        result = alumnos.alumno_by_id(data['padron'])
        if len(result) > 0:
            return jsonify({'error': 'El alumno ya existe'}), 400

        insert_alumno(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(data), 201


@app.route('/api/v1/alumnos/<int:padron>', methods=['PUT'])
def update_alumno(padron):
    data = request.get_json()

    keys = ('nombre', 'apellido')
    for key in keys:
        if key not in data:
            return jsonify({'error': f'Falta el dato {key}'}), 400

    try:
        result = alumnos.alumno_by_id(padron)
        if len(result) == 0:
            return jsonify({'error': 'No se encontró el alumno'}), 404

        alumnos.actualizar_alumno(padron, data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'padron': padron, **data}), 200


@app.route('/api/v1/alumnos/<int:padron>', methods=['DELETE'])
def delete_alumno(padron):
    try:
        result = alumnos.alumno_by_id(padron)
        if len(result) == 0:
            return jsonify({'error': 'No se encontró el alumno'}), 404

        alumnos.borra_alumno(padron)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    result = result[0]
    return jsonify({'nombre': result[0], 'apellido': result[1], 'padron': padron}), 200


@app.route('/api/v1/alumnos/search', methods=['GET'])
def search_alumnos():
    try:
        result = alumnos.buscar_alumnos(request.args)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({'padron': row[0], 'nombre': row[1], 'apellido': row[2]})

    return jsonify(response), 200


@app.route('/api/v1/notas/<string:nombre>/<string:apellido>', methods=['GET'])
def get_notas_by_alumno(nombre, apellido):
    try:
        result = alumnos.notas_by_alumno(nombre, apellido)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    response = []
    for row in result:
        response.append({'nota': row[0], 'nombre': row[1], 'apellido': row[2]})

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True)
