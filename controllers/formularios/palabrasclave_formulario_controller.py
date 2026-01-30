################################################################################################
################################################################################################
from flask import Blueprint, render_template, request, redirect, flash
from database.db import get_db

palabrasclave_formulario_bp = Blueprint("palabrasclave_formulario_bp",__name__)

# ======================================================
# 1. FORMULARIO DE CREACIÓN
# ======================================================
@palabrasclave_formulario_bp.route("/crear-palabra", methods=["GET"])
def mostrar_formulario_palabra():
    return render_template("formularios/palabrasclave_formulario.html")

@palabrasclave_formulario_bp.route("/crear-palabra", methods=["POST"])
def procesar_formulario_palabra():
    palabra = request.form.get("palabra")
    descripcion = request.form.get("descripcion")
    respuesta = request.form.get("respuesta")

    if not palabra or not descripcion or not respuesta:
        flash("Todos los campos son obligatorios.", "danger")
        return redirect("/crear-palabra")

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO PALABRA_CLAVE (Palabra, Descripcion, Respuesta_designada)
            VALUES (%s, %s, %s);
        """, (palabra, descripcion, respuesta))

        conn.commit()
        flash("Palabra clave creada correctamente.", "success")

    except Exception as e:
        flash(f"Error al crear: {e}", "danger")

    finally:
        conn.close()

    return redirect("/palabras-clave")


# ======================================================
# 2. FORMULARIO DE EDICIÓN
# ======================================================

@palabrasclave_formulario_bp.route("/editar-palabra/<int:id>", methods=["GET"])
def mostrar_formulario_editar_palabra(id):
    """
    Muestra el formulario de edición con los datos cargados.
    """
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM PALABRA_CLAVE WHERE ID = %s", (id,))
    palabra = cursor.fetchone()

    conn.close()

    if not palabra:
        flash("La palabra clave no existe.", "danger")
        return redirect("/palabras-clave")

    return render_template("formularios/palabrasclave_editar.html", palabra=palabra)


@palabrasclave_formulario_bp.route("/editar-palabra/<int:id>", methods=["POST"])
def procesar_edicion_palabra(id):
    """
    Procesa los cambios del formulario de edición.
    """
    palabra = request.form.get("palabra")
    descripcion = request.form.get("descripcion")
    respuesta = request.form.get("respuesta")

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE PALABRA_CLAVE
            SET Palabra = %s,
                Descripcion = %s,
                Respuesta_designada = %s
            WHERE ID = %s;
        """, (palabra, descripcion, respuesta, id))

        conn.commit()
        flash("Cambios guardados correctamente.", "success")

    except Exception as e:
        flash(f"Error al actualizar: {e}", "danger")

    finally:
        conn.close()

    return redirect("/palabras-clave")

################################################################################################
################################################################################################