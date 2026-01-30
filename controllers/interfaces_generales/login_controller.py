## Por Alfonso Espinoza
###################################################
from flask import Blueprint, render_template, request, redirect, url_for
from database.db import get_db
###################################################
login_bp = Blueprint("login_bp", __name__)
###################################################
###################################################
@login_bp.route("/", methods=["GET", "POST"])
def login():

    # SI ENTRA POR GET → mostrar formulario
    if request.method == "GET":
        return render_template("interfaces_generales/login.html")

    # SI ENTRA POR POST → procesar login
    username = request.form.get("username")
    password = request.form.get("password")

    # VALIDACIÓN SIMPLE prototipo
    if username == "Admin" and password == "1234":
        return render_template("/interfaces_generales/home.html")
    #redirect(url_for("/interfaces_generales/home.html"))  # o al panel principal
    else:
        error = "Usuario o contraseña incorrectos"
        return render_template(
            "interfaces_generales/login.html",
            error=error


        )
###################################################
# ============================================================
# 1. LISTAR SOLICITANTES
# ============================================================
@login_bp.route("/panel-solicitantes")
def panel_solicitantes():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Administrador_Secretaria")
    solicitantes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "registros_crud/solicitantes_tabla.html",
        solicitantes=solicitantes
    )
############################
@login_bp.route("/home")
def home():
    return render_template("/interfaces_generales/home.html")
############################
##from flask import Blueprint, render_template, session, redirect

