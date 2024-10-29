from sqlalchemy import text, create_engine

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

def run_query(query, parameters=None):
    with engine.connect() as conn:
        result = conn.execute(text(query), parameters)
        conn.commit()

    return result

def all_alumnos():
    return run_query(QUERY_TODOS_LOS_ALUMNOS).fetchall()

def alumno_by_id(padron):
    return run_query(QUERY_ALUMNO_BY_ID, {'padron': padron}).fetchall()


def insert_alumno(data):
    run_query(QUERY_INGRESAR_ALUMNO, data)


def actualizar_alumno(padron, data):
    run_query(text(QUERY_ACTUALIZAR_ALUMNO), {'padron': padron, **data})


def borra_alumno(padron):
    run_query(text(QUERY_BORRAR_ALUMNO), {'padron': padron})


def buscar_alumnos(argumentos):
    query = QUERY_TODOS_LOS_ALUMNOS

    filtros = " AND ".join([f"{key} = '{value}' " for key, value in argumentos.items()])
    filtros = f" WHERE {filtros}" if len(filtros) > 0 else ""

    query += filtros

    return run_query(query).fetchall()


def notas_by_alumno(nombre, apellido):
    return run_query(QUERY_NOTA_POR_ALUMNO, {'nombre': nombre, 'apellido': apellido}).fetchall()


