from flask import Blueprint, render_template, request, redirect, flash
from database.db import get_db

palabras_bp = Blueprint("palabras_bp", __name__)

# ======================================================
# LISTAR PALABRAS
# ======================================================
@palabras_bp.route("/registros_crud/palabrasclave_tabla")
def listar_palabras():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM PALABRA_CLAVE")
    palabras = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "registros_crud/palabrasclave_tabla.html",
        palabras=palabras
    )

# ======================================================
# BUSCAR PALABRAS
# ======================================================
@palabras_bp.route("/buscar-palabras")
def buscar_palabras():
    query = request.args.get("q", "")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM PALABRA_CLAVE
        WHERE Palabra LIKE %s OR Descripcion LIKE %s
    """, (f"%{query}%", f"%{query}%"))

    palabras = cursor.fetchall()
    conn.close()

    return render_template("registros_crud/palabrasclave_tabla.html", palabras=palabras)

# ======================================================
# FORMULARIO CREAR
# ======================================================

###Ojos, Roberto. Con esto de acá se le pone nombre y dirección
# a esta cochinada de archvio.
@palabras_bp.route("/palabras_clave", methods=["GET"])
def mostrar_tabla_palabras():
    return render_template("registros_crud/palabrasclave_tabla.html")

# ======================================================
# PROCESAR CREACIÓN
# ======================================================
@palabras_bp.route("/crear-palabra", methods=["POST"])
def guardar_palabra():
    palabra = request.form["Palabra"]
    descripcion = request.form["Descripcion"]
    respuesta = request.form["Respuesta_designada"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO PALABRA_CLAVE (Palabra, Descripcion, Respuesta_designada)
        VALUES (%s, %s, %s)
    """, (palabra, descripcion, respuesta))

    conn.commit()
    conn.close()

    return redirect("/palabras")

# ======================================================
# FORMULARIO EDITAR
# ======================================================
@palabras_bp.route("/editar-palabra/<int:id_pc>")
def editar_palabra(id_pc):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM PALABRA_CLAVE WHERE ID_PC = %s", (id_pc,))
    palabra = cursor.fetchone()
    conn.close()

    return render_template("editar_palabra.html", palabra=palabra)

# ======================================================
# PROCESAR EDICIÓN
# ======================================================
@palabras_bp.route("/editar-palabra/<int:id_pc>", methods=["POST"])
def actualizar_palabra(id_pc):
    palabra = request.form["Palabra"]
    descripcion = request.form["Descripcion"]
    respuesta = request.form["Respuesta_designada"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE PALABRA_CLAVE
        SET Palabra=%s, Descripcion=%s, Respuesta_designada=%s
        WHERE ID_PC=%s
    """, (palabra, descripcion, respuesta, id_pc))

    conn.commit()
    conn.close()

    return redirect("/palabras")

# ======================================================
# ELIMINAR
# ======================================================
@palabras_bp.route("/eliminar-palabra/<int:id_pc>")
def eliminar_palabra(id_pc):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM PALABRA_CLAVE WHERE ID_PC = %s", (id_pc,))
    conn.commit()
    conn.close()

    return redirect("/palabras")