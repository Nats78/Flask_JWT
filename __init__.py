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
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
# Configuration du module JWT
app.config["JWT_SECRET_KEY"] = "Ma_clé_secrete"  # Clé secrète pour signer les tokens
jwt = JWTManager(app)

# Fonction pour ajouter des rôles dans le JWT
def add_role_to_token(username, role):
    # On ajoute le rôle dans le token comme claim supplémentaire
    return create_access_token(identity=username, additional_claims={"role": role})

@app.route('/')
def hello_world():
    return render_template('accueil.html') 

# Création d'une route qui vérifie l'utilisateur et retour un Jeton JWT si ok.
# La fonction create_access_token() est utilisée pour générer un jeton JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401

    access_token = create_access_token(identity=username, expires_delta=False)
    return jsonify(access_token=access_token)

# Route protégée par un jeton valide
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
                                                                                                               
if __name__ == "__main__":
  app.run(debug=True)
