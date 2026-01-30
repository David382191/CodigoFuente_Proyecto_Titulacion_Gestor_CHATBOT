############################################################################################
############################################################################################
from flask import Blueprint, render_template, flash, request, redirect
from mysql.connector import Error
from database.db import get_db
from psycopg2.extras import RealDictCursor

secretaria_bp = Blueprint('secretaria_bp', __name__)

# ============================================================
# 1. LISTAR TODAS LAS SECRETARIAS
# ============================================================


@secretaria_bp.route("/lista_secretarias")
def lista_secretarias():
    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # 1️⃣ ¿Qué base de datos es?
    cursor.execute("SELECT current_database() AS db")
    print("📌 BASE DE DATOS:", cursor.fetchone())

    # 2️⃣ ¿Cuántos registros hay?
    cursor.execute("SELECT COUNT(*) AS total FROM admin_secretaria")
    print("📌 TOTAL REGISTROS:", cursor.fetchone())

    # 3️⃣ Traer datos reales
    cursor.execute("""
        SELECT
            cedula   AS "CEDULA",
            nombre   AS "Nombre",
            apellido AS "Apellido",
            usuario  AS "Usuario",
            telefono AS "Telefono"
        FROM admin_secretaria
    """)
    secretarias = cursor.fetchall()
    print("📌 DATOS:", secretarias)

    cursor.close()
    conn.close()

    return render_template(
        "registros_crud/secretaria_tabla.html",
        secretarias=secretarias
    )
# ============================================================
# 2. BUSCAR SECRETARIA (por nombre / cedula / tipo)
# ============================================================
@secretaria_bp.route("/buscar-secretaria")
def buscar_secretaria():
    q = request.args.get("q", "")

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT * FROM admin_secretaria
        WHERE cedula LIKE %s
           OR nombre LIKE %s
           OR apellido LIKE %s
    """

    like = f"%{q}%"
    cursor.execute(sql, (like, like, like))
    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "registros_crud/secretaria_tabla.html",
        secretarias=resultados
    )

# ==========================
# 3. ELIMINAR SECRETARIA.
# ==========================
@secretaria_bp.route("/eliminar-secretaria/<cedula>")
def eliminar_secretaria(cedula):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM ADMIN_SECRETARIA WHERE CEDULA=%s", (cedula,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/secretaria_tabla")

# ==========================
#  4. TRAER INFORMACIÓN DE LA SECRETARIA
# ==========================
@secretaria_bp.route("/editar/<cedula>", methods=["GET"])
def traerinformacion(cedula):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # GET → llenar formulario
    cursor.execute("SELECT * FROM admin_secretaria WHERE CEDULA=%s", (cedula,))
    secretaria_editar = cursor.fetchone()

    cursor.close()
    conn.close()

    print("CEDULA RECIBIDA:", cedula)
    print("SECRETARIA:", secretaria_editar)

    return render_template("editables/secretaria_editar.html", secretaria_editar=secretaria_editar)

# =================================
#  5. IR A CREAR NUEVA SECRETARIA.
# =================================
@secretaria_bp.route("/ir-crear-secretaria", methods=["GET", "POST"])
def ir_crear_secretaria():
    
    return render_template("formularios/secretaria_formulario.html")
#    pass
############################################################################################
############################################################################################
##what does a men who is about to die think.
##It dopends. How he's going to die. Why he's dying.
## If he is going to kill himself.
## He may tought how here's nothing left for him.
## And hope there is something waiting for him in the other side.