from typing import Any
 from typing import Optional
 import jwt
 from flask import Flask  #Commentaire de mise à jour.
 from flask import Flask  
 from flask import render_template
 from flask import json
 from flask import jsonify
 @@ -15,6 +15,7 @@
 from flask_jwt_extended.typing import Fresh
 from flask_jwt_extended import create_access_token
 from flask_jwt_extended import get_jwt_identity
 from flask_jwt_extended import get_jwt
 from flask_jwt_extended import jwt_required
 from flask_jwt_extended import JWTManager
 
 @@ -35,11 +36,11 @@ def hello_world():
 def login():
     username = request.json.get("username", None)
     password = request.json.get("password", None)
     role = request.json.get("role", "user")  # Récupération du rôle, par défaut "user"
     if username != "test" or password != "test":
         return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401
 
     access_token = create_access_token(identity=username, expires_delta=False)
 
     return jsonify(access_token=access_token)
 
 
 @@ -49,6 +50,24 @@ def login():
 def protected():
     current_user = get_jwt_identity()
     return jsonify(logged_in_as=current_user), 200
 
 # Middleware pour vérifier le rôle de l'utilisateur
 def role_required(required_role):
     def wrapper(fn):
         @jwt_required()
         def decorator(*args, **kwargs):
             claims = get_jwt()
             if claims.get("role") != required_role:
                 return jsonify({"msg": "Accès interdit : rôle insuffisant"}), 403
             return fn(*args, **kwargs)
         return decorator
     return wrapper
 
 # Route accessible uniquement aux administrateurs
 @app.route("/admin", methods=["GET"])
 @role_required("admin")
 def admin():
     return jsonify({"msg": "Bienvenue sur la page admin"}), 200
 
 if __name__ == "__main__":
