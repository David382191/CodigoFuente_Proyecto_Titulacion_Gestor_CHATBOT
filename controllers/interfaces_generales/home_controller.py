################################################################################
from flask import Blueprint, render_template, redirect, url_for

home_bp = Blueprint("home_bp", __name__)
################################################################
@home_bp.route('/home')
def home():
    return render_template('interfaces_generales/home.html')
################################################################
@home_bp.route("/solicitantes_tabla")  
def panel_solicitantes():
    return redirect(url_for("solicitantes_bp.listar_solicitantes"))

##Oye, Roberto. este nombre de arriba ni dea de que con tiene que coindidir
@home_bp.route("/secretaria_tabla")
def panel_administradores():
    ##Pero esto de acá tiene que coincidir con el controlador que quierar abrir.
    return redirect(url_for("secretaria_bp.lista_secretarias"))

@home_bp.route("/conversaciones_tabla")
def panel_conversaciones():
    return redirect(url_for("conversaciones_bp.listar_conversaciones"))

@home_bp.route("/mensajes_tabla")
def panel_mensajes():
    return redirect(url_for("mensajes_bp.listar_mensajes"))

@home_bp.route("/palabrasclave_tabla")
def panel_palabras_clave():
    return redirect(url_for("palabras_bp.listar_palabras"))

@home_bp.route("/salir")
def salir():
    return render_template("interfaces_generales/login.html")
################################################################################