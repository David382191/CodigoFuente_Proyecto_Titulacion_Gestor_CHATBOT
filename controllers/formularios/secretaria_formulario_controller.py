###################################################################################################
from flask import Blueprint, render_template, request, redirect, url_for, flash, Flask
from werkzeug.security import generate_password_hash
from database.db import get_db
import mysql.connector

# Blueprint
secretaria_form_bp = Blueprint("secretaria_form_bp", __name__)

# ==========================
# 1. MOSTRAR FORMULARIO
# ==========================
@secretaria_form_bp.route("/nueva-secretaria")
def nueva_secretaria():
    return render_template("secretaria_formulario.html")

# ==========================
# 2. PROCESAR FORMULARIO
# ==========================
@secretaria_form_bp.route("/crear-secretaria", methods=["GET", "POST"])
def crear_secretaria():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        # 🔴 VALIDACIÓN (AQUÍ VA)
        cedula = request.form.get("CEDULA", "").strip()
        nombre = request.form.get("Nombre", "").strip()
        apellido = request.form.get("Apellido", "").strip()
        usuario = request.form.get("Usuario", "").strip()
        contrasena = request.form.get("Contrasena_hash", "").strip()
        telefono = request.form.get("Telefono", "").strip()

        if not cedula or not nombre or not apellido or not usuario or not telefono:
            flash("Todos los campos son obligatorios", "danger")
            cursor.close()
            conn.close()
            return redirect(request.url)

        # 🟢 INSERT SOLO SI TODO ESTÁ BIEN
        cursor.execute("""
            INSERT INTO admin_secretaria
            (CEDULA, Nombre, Apellido, Usuario, Contrasena_hash, Telefono)
            VALUES (%s, %s, %s, %s,%s, %s)
        """, (cedula, nombre, apellido, usuario, contrasena, telefono))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("home_bp.panel_administradores"))

    return render_template("registro_crud/secretaria_tabla_controller.html")

###################################################################################################
@secretaria_form_bp.route('/agregar-admin', methods=['POST'])
def agregar_admin():

    conn = get_db()
    cursor = conn.cursor(dictionary=True)


    cedula = request.form['cedula']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']  # recordar hashear
    telefono = request.form['telefono']

    # 1️⃣ Validar CEDULA
    cursor.execute("SELECT COUNT(*) FROM ADMIN_SECRETARIA WHERE CEDULA = %s", (cedula,))
    (count_cedula,) = cursor.fetchone()
    if count_cedula > 0:
        flash("¡Error! Ya existe un admin con esa cédula.", "danger")
        return redirect("/secretaria_tabla")

    # 2️⃣ Validar USUARIO
    cursor.execute("SELECT COUNT(*) FROM ADMIN_SECRETARIA WHERE Usuario = %s", (usuario,))
    (count_usuario,) = cursor.fetchone()
    if count_usuario > 0:
        flash("¡Error! El nombre de usuario ya está en uso.", "danger")
        return redirect("/secretaria_tabla")

    # 3️⃣ Insertar registro si todo está bien
    cursor.execute("""
        INSERT INTO ADMIN_SECRETARIA (CEDULA, Nombre, Apellido, Usuario, Contrasena_hash, Telefono)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (cedula, nombre, apellido, usuario, contrasena, telefono))
    conn.commit()

    flash("Admin agregado correctamente", "success")
    return redirect("/secretaria_tabla")
