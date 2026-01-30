#################################################################################################
#################################################################################################
from flask import Blueprint, render_template, request, redirect
from database.db import get_db

solicitante_form_bp = Blueprint("solicitante_form_bp", __name__)

# ============================================================
# 1. LISTAR SOLICITANTES
# ============================================================
@solicitante_form_bp.route("/panel-solicitantes")
def panel_solicitantes():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM SOLICITANTE")
    solicitantes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "registros_crud/solicitantes_tabla.html",
        solicitantes=solicitantes
    )

# ============================================================
# 2. MOSTRAR FORMULARIO PARA MODIFICAR SOLICITANTE
# ============================================================
@solicitante_form_bp.route("/modificar-solicitante/<cedula>", methods=["GET"])
def mostrar_modificacion(cedula):
    
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM SOLICITANTE WHERE CEDULA=%s", (cedula,))
    solicitante = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "formularios/modificar_solicitante.html",  # usa tu HTML
        solicitante=solicitante
    )

# ============================================================
# 3. GUARDAR CAMBIOS DE SOLICITANTE
# ============================================================
@solicitante_form_bp.route("/modificar-solicitante/<cedula>", methods=["POST"])
def guardar_modificacion(cedula):
    nombre = request.form["Nombre"]
    telefono = request.form["Telefono"]
    tipo = request.form["Tipo_solicitante"]

    conn = get_db()
    cursor = conn.cursor()

    sql = """
        UPDATE SOLICITANTE
        SET Nombre=%s, Telefono=%s, Tipo_solicitante=%s
        WHERE CEDULA=%s
    """

    cursor.execute(sql, (nombre, telefono, tipo, cedula))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/panel-solicitantes")



#################################################################################################
#################################################################################################
##what does a men who is about to die think.
##It dopends. How he's going to die. Why he's dying.
## If he is going to kill himself.
## He may tought how here's nothing left for him.
## And hope there is something waiting for him in the other side.