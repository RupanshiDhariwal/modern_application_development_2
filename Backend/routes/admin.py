from flask_restful import Resource
from flask import request , jsonify, make_response
from flask_security import roles_accepted, auth_token_required

from models import db, user_datastore, User,Influencer,Sponsor

class activateSponsor(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def post(self,id):
        user = user_datastore.find_user(id=id)
        if user and user.has_role('sponsor'):
            user_datastore.activate_user(user)
            db.session.commit()
            return jsonify({"message": "User activated successfully"})
        return jsonify({"message":"User not found"})

class activeUser(Resource):
    @auth_token_required
    # @roles_accepted('admin')
    def get(self):
        users = User.query.filter_by(active=1).all()
        
        if users:
            # Assuming User has a `serialize` method
            return jsonify([user.serialize() for user in users])
        
        return jsonify({"result": [], "message": "No user found"})
    
class DeactivateUser(Resource):
    @auth_token_required
    @roles_accepted('admin')  # Uncomment if only admin users can perform this action
    def post(self,id):
        # Get user ID from the request
        user_id = id
        
        if not user_id:
            return make_response(jsonify({"message": "User ID is required"}), 400)
        
        # Fetch the user by ID
        user = User.query.get(user_id)
        
        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)
        
        if user.active == 0:
            return make_response(jsonify({"message": "User is already inactive"}), 400)
        
        # Deactivate the user
        user.active = 0
        db.session.commit()
        
        return make_response(jsonify({"message": "User has been deactivated"}), 200)
    
class AllUsers(Resource):
    from caching import cache
    @auth_token_required
    @roles_accepted('admin')
    @cache.cached(timeout=30)
    def get(self):
        users = User.query.all()

        # Filter out admin users
        non_admin_users = [user for user in users if not any(role.name == 'admin' for role in user.roles)]

        # Calculate total counts of influencers and sponsors
        influencer_count = Influencer.query.count()
        sponsor_count = Sponsor.query.count()

        # Serialize the data
        data = [user.serialize() for user in non_admin_users]
        
        # Return the response with counts included
        return make_response(jsonify({
            "message": "got user list",
            "data": data,
            "total_influencers": influencer_count,
            "total_sponsors": sponsor_count
        }), 200)
    

class DeactivatedSponsors(Resource):
    @auth_token_required
    @roles_accepted('admin')
    def get(self):
        # Query to get all deactivated sponsors
        deactivated_sponsors = User.query.join(Sponsor).filter(User.active == 0).all()

        # Serialize the data with selected fields
        data = [
            {
                "id": user.id,
                "email": user.email,
                "company_name": user.sponsor.company_name if user.sponsor else None,
                "individual_name": user.sponsor.individual_name if user.sponsor else None,
                "industry": user.sponsor.industry if user.sponsor else None,
                "budget": user.sponsor.budget if user.sponsor else None,
                "username": user.username
            }
            for user in deactivated_sponsors
        ]

        # Return the response
        return make_response(jsonify({
            "message": "Got deactivated sponsors list",
            "data": data
        }), 200)