from flask import Flask
from flask import render_template
from flask import json
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended.typing import ExpiresDelta                                                                                                                                       
from flask import Flask, render_template, jsonify, request

import datetime  # Import nécessaire pour la gestion de l'expiration des tokens

app = Flask(__name__)

# Configuration du module JWT
app.config["JWT_SECRET_KEY"] = "Ma_clé_secrete"  # Clé secrète pour signer les tokens
jwt = JWTManager(app)

@app.route('/')
def hello_world():
    return render_template('accueil.html') 

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username != "test" or password != "test":
        return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401

    role = "admin" if username == "admin" else "user"  # Attribution du rôle

    # Création du token JWT avec le rôle de l'utilisateur
    access_token = create_access_token(identity=username, additional_claims={"role": role})
    return jsonify(access_token=access_token)

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route("/admin", methods=["GET"])
@jwt_required()
def admin():
    claims = get_jwt()  # Récupération des données du token
    if claims.get("role") != "admin":
        return jsonify({"msg": "Accès refusé : vous devez être admin"}), 403
    return jsonify(msg="Bienvenue, administrateur !"), 200

if __name__ == "__main__":
    app.run(debug=True)
