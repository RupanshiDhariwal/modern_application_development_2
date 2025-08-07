from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import login_user
from datetime import datetime

from models import db, user_datastore, User, Sponsor,Influencer

class signup(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        user = user_datastore.find_user(email=email)
        if not user:
            user = user_datastore.create_user(email=email,password = password)
            if role == "sponsor":
                user_datastore.add_role_to_user(user,"sponsor")
                user_datastore.deactivate_user(user)

                # Create a new Sponsor entry with default values
                sponsor = Sponsor(user_id=user.id, company_name=None, individual_name=None, industry=None, budget=None)
                db.session.add(sponsor)
                

            elif role == "influencer":
                user_datastore.add_role_to_user(user, 'influencer')

                # Create a new Influencer entry with default values
                influencer = Influencer(user_id=user.id, name=None, category=None, niche=None, reach=None)
                db.session.add(influencer)

            db.session.commit()
            return jsonify({"message":"User registered successfully"})
        return jsonify({"message":"User already exists"})


class login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = user_datastore.find_user(email = email)
        if user:
            if not user.active:
                return make_response(jsonify({"message": "You are not approved by admin yet"}), 403)
            from flask_security.utils import verify_password
            if verify_password(password, user.password):
                print(user.roles)
                login_user(user)
        
               # Update last_login_at
                user.last_login_at = datetime.utcnow()
                db.session.commit()
                roles = [role.name for role in user.roles] 
                return make_response(jsonify({"message":"Login successful","authToken": user.get_auth_token(),"roles": roles, "userId": user.id}), 200)
            return make_response(jsonify({"message":"invalid email/password"}), 401)
        return make_response(jsonify({"message":"Please register before login"}), 401)