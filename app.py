from flask import Flask, render_template, request, jsonify, redirect, url_for
from entities.accont import Account
from entities.user import User
from entities.transaction import Transaction
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from dotenv import load_dotenv
import os
from decimal import Decimal

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"

@login_manager.user_loader
def load_user(id_user):
    return User.get_by_id(id_user)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route('/welcome', methods=["GET"])
@login_required
def welcome():
    # Obtener la cuenta del usuario actual en base a su ID
    account = Account.get_by_user_id(current_user.id)
    # Obtener las transacciones de la cuenta en un array
    transacciones = []
    saldo = None    # por si no tiene cuenta
    if account:
        # Obtener las transacciones de la cuenta en un array
        transacciones = Transaction.get_by_account(account.id)
        saldo = Decimal('0.0')
        for t in transacciones:
            # Si el tipo de transacción es 1, se suma el monto al saldo
            if t.type == 1:
                saldo += Decimal(t.amount)
            # Si el tipo de transacción es 2, se resta el monto al saldo
            elif t.type == 2:
                saldo -= Decimal(t.amount)
    # Renderizar la plantilla de bienvenida con la cuenta, el saldo y las transacciones
    return render_template('welcome.html', account=account, saldo=float(saldo) if saldo is not None else None, transacciones=transacciones)

@app.route('/api/users', methods=["POST"])
def create_user():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if User.check_email_exists(email):
        return jsonify({"success": False, "message": "El correo electrónico ingresado ya se encuentra registrado."}), 409

    if User.save(name, email, password):
        return jsonify({"success": True, "message": "Su cuenta fue creada correctamente."}), 201
    else:
        return jsonify({"success": False, "message": "Ocurrió un error al crear su cuenta. Intente de nuevo"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.check_login(email, password)
    if user:

        login_user(user)
        return jsonify({
            "success": True,
            "message": "Sesión iniciada correctamente"
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "Los datos de acceso ingresados no son correctos."
        }), 401



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

"""@app.route("/api/welcome", methods=["GET"])
@login_required
def check_account():
    user_id = int(request.cookies.get("id"))
    has_account = Account.check_account(user_id)

    return jsonify({"has_account": has_account}), 200
"""


if __name__ == '__main__':
    app.run()