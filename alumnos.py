from sqlalchemy import text, create_engine
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

def all_alumnos():
    conn = Session()
    result = conn.execute(text(QUERY_TODOS_LOS_ALUMNOS)).fetchall()
    conn.close()

    return result

def alumno_by_id(padron):
    conn = Session()
    result = conn.execute(text(QUERY_ALUMNO_BY_ID), {'padron': padron}).fetchall()
    conn.close()

    return result


def insert_alumno(data):
    conn = Session()
    conn.execute(text(QUERY_INGRESAR_ALUMNO), params=data)
    conn.commit()
    conn.close()


def actualizar_alumno(padron, data):
    conn = Session()
    conn.execute(text(QUERY_ACTUALIZAR_ALUMNO), params={'padron': padron, **data})
    conn.commit()
    conn.close()


def borra_alumno(padron):
    conn = Session()
    conn.execute(text(QUERY_BORRAR_ALUMNO), {'padron': padron})
    conn.commit()
    conn.close()


def buscar_alumnos(argumentos):
    query = QUERY_TODOS_LOS_ALUMNOS

    filtros = " AND ".join([f"{key} = '{value}' " for key, value in argumentos.items()])
    filtros = f" WHERE {filtros}" if len(filtros) > 0 else ""

    query += filtros

    conn = Session()
    result = conn.execute(text(query)).fetchall()
    conn.close()

    return result


def notas_by_alumno(nombre, apellido):
    conn = Session()
    result = conn.execute(text(QUERY_NOTA_POR_ALUMNO), {'nombre': nombre, 'apellido': apellido}).fetchall()
    conn.close()

    return result


