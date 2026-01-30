#################################################################################################
#################################################################################################

# controller_mensajes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.db import get_db

mensajes_bp = Blueprint("mensajes_bp", __name__)

# ============================================================
# LISTAR MENSAJES DE UNA CONVERSACIÓN
# ============================================================

@mensajes_bp.route("/listar_mensajes")
def listar_mensajes():

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM MENSAJE ORDER BY Fecha_hora DESC")
    
    m = cursor.fetchall()
    ##print("📌 DATOS:", mensajes) La información sí se está trayendo, todo bien por aquí.
    
    cursor.close()
    conn.close()

    return render_template("registros_crud/mensajes_tabla.html", m=m)

# ============================================================
# LISTAR MENSAJES DE UNA CONVERSACIÓN
# ============================================================
@mensajes_bp.route("/buscar-mensajes")
def buscar_mensajes():
    q = request.args.get("q", "")

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT * FROM MENSAJE
        WHERE ID_MENSAJE LIKE %s
           OR ID_CONVERSACION LIKE %s
           OR Remitente LIKE %s
           OR Fecha_hora LIKE %s
    """

    like = f"%{q}%"
    cursor.execute(sql, (like, like, like, like))
    m = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "registros_crud/mensajes_tabla.html",
        m=m
    )
################################################################################################
################################################################################################