from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import current_user
from datetime import datetime
from flask_security import roles_accepted, auth_token_required

from models import db, Ad_request, UserAdRequest, AdRequestNegotiation, Influencer



class Influencers(Resource):
    @auth_token_required
    @roles_accepted('sponsor', 'influencer')
    def post(self):
        data = request.get_json()
        print('data', data)
        print('current_user', current_user.id)
        name = data.get('name')
        category = data.get('category')
        niche = data.get('niche')
        reach = data.get('reach')

        if not (name and category and niche and reach):
            return make_response(jsonify({"message": "Please fill all required fields"}), 403)

        influencer = Influencer.query.filter_by(name=name).first()

        if not influencer:
            new_influencer = Influencer(
                name=name,
                category=category,
                niche=niche,
                reach=reach,
                user_id=current_user.id
            )
            db.session.add(new_influencer)
            db.session.commit()
            return make_response(jsonify({
                "message": "Influencer profile created successfully"
            }), 201)
        return jsonify({
            "message": "An influencer with this name already exists"
        })

    @auth_token_required
    def get(self):
        influencers = Influencer.query.all()
        data = [inf.serialize() for inf in influencers]

        if not data:
            return make_response(jsonify({"message": "No influencers found", "data": []}))

        return make_response(jsonify({"message": "Got influencer list", "data": data})) 

class AcceptRequest(Resource):
    @auth_token_required
    @roles_accepted('sponsor', 'influencer')
    def put(self, id):
        print('working1')
        ad_request = Ad_request.query.filter_by(id=id).first()
        print('working2')

        if not ad_request:
            return make_response(jsonify({"message": "ad_request not found with this id"}), 404)

        ad_request.status = "accepted"

        # Use current_user from Flask-Security
        if not current_user:
            return make_response(jsonify({"message": "User not found"}), 404)

        # Create a new UserAdRequest entry
        user_ad_request = UserAdRequest(
            user_id=current_user.id,
            ad_request_id=ad_request.id,
            status='accepted',
            response_date=datetime.now()
        )
        
        # Add to the session and commit
        db.session.add(user_ad_request)
        db.session.commit()
        
        return make_response(jsonify({"message": "ad_request Accepted successfully"}), 200)


class InfluencerSpecific(Resource):
    # @auth_token_required
    def put(self, id):
        influencer = Influencer.query.filter_by(user_id=id).first()

        if not influencer:
            return make_response(jsonify({"message": "Influencer not found with this id"}), 404)

        data = request.get_json()
        name = data.get('name')
        category = data.get('category')
        niche = data.get('niche')
        reach = data.get('reach')

        if not (name and category and niche and reach):
            return make_response(jsonify({"message": "Please fill all required fields"}), 403)

        influencer.name = name
        influencer.category = category
        influencer.niche = niche
        influencer.reach = reach
        db.session.commit()

        return make_response(jsonify({"message": "Influencer profile updated successfully"}), 200)

    # @auth_token_required
    def get(self, id):
        influencer = Influencer.query.filter_by(user_id=id).first()
        if not influencer:
            return make_response(jsonify({"message": "No influencer found with this id"}), 404)

        return make_response(jsonify({"message": "Got specific influencer", "data": influencer.serialize()}), 200)

    

class RejectRequest(Resource):
    @auth_token_required
    @roles_accepted('sponsor','influencer')
    def put(self,id):
        print('working1')
        ad_request = Ad_request.query.filter_by(id=id).first()
        print('working2')

        if not ad_request:
            return make_response(jsonify({"message":"ad_request not found with this id"}),404)
        
        if not current_user:
            return make_response(jsonify({"message": "User not found"}), 404)

        # Create a new UserAdRequest entry
        user_ad_request = UserAdRequest(
            user_id=current_user.id,
            ad_request_id=ad_request.id,
            status='rejected',
            response_date=datetime.now()
        )
        
        # Add to the session and commit
        db.session.add(user_ad_request)
        db.session.commit()
        
        return make_response(jsonify({"message":"ad_request rejected successfully"}), 200)
    

class AcceptNegotiation(Resource):
    @auth_token_required
    @roles_accepted('sponsor', 'influencer')
    def put(self, negotiation_id):
        # Fetch the AdRequestNegotiation entry
        negotiation = AdRequestNegotiation.query.filter_by(id=negotiation_id).first()

        if not negotiation:
            return make_response(jsonify({"message": "Negotiation not found with this id"}), 404)

        # Fetch the associated AdRequest
        ad_request = Ad_request.query.filter_by(id=negotiation.ad_request_id).first()

        if not ad_request:
            return make_response(jsonify({"message": "Ad Request not found"}), 404)

        # Get the current user (assuming you have a way to get the current user, such as from the token)
        current_user = get_current_user()
        
        if not current_user:
            return make_response(jsonify({"message": "User not found"}), 404)

        # Update the negotiation status based on the user's role
        if current_user.has_role('influencer'):
            if negotiation.influencer_negotiation_status == 'pending':
                negotiation.influencer_negotiation_status = 'accepted'
                # Also update the AdRequestNegotiation entry to reflect the influencer's acceptance
                negotiation.should_nego_status_change_influencer = False
            else:
                return make_response(jsonify({"message": "Negotiation is not pending for influencer"}), 400)
        
        elif current_user.has_role('sponsor'):
            if negotiation.sponsor_negotiation_status == 'pending':
                negotiation.sponsor_negotiation_status = 'accepted'
                # Also update the AdRequestNegotiation entry to reflect the sponsor's acceptance
                negotiation.should_nego_status_change_sponsor = False
            else:
                return make_response(jsonify({"message": "Negotiation is not pending for sponsor"}), 400)

        # Create or update the UserAdRequest entry
        user_ad_request = UserAdRequest.query.filter_by(
            user_id=current_user.id,
            ad_request_id=ad_request.id
        ).first()

        if user_ad_request:
            user_ad_request.status = 'accepted'
            user_ad_request.response_date = datetime.now()
        else:
            user_ad_request = UserAdRequest(
                user_id=negotiation.created_by,
                ad_request_id=ad_request.id,
                status='accepted',
                response_date=datetime.now()
            )
            db.session.add(user_ad_request)
        ad_request.status="accepted"
        # Commit the changes to the database
        db.session.commit()

        return make_response(jsonify({"message": "Negotiation accepted and updated successfully"}), 200)
    

class RejectNegotiation(Resource):
    @auth_token_required
    @roles_accepted('sponsor', 'influencer')
    def put(self, negotiation_id):
        # Fetch the AdRequestNegotiation entry
        negotiation = AdRequestNegotiation.query.filter_by(id=negotiation_id).first()

        if not negotiation:
            return make_response(jsonify({"message": "Negotiation not found with this id"}), 404)

        # Fetch the associated AdRequest
        ad_request = Ad_request.query.filter_by(id=negotiation.ad_request_id).first()

        if not ad_request:
            return make_response(jsonify({"message": "Ad Request not found"}), 404)

        # Get the current user (assuming you have a way to get the current user, such as from the token)
        current_user = get_current_user()
        
        if not current_user:
            return make_response(jsonify({"message": "User not found"}), 404)

        # Update the negotiation status based on the user's role
        if current_user.has_role('influencer'):
            if negotiation.influencer_negotiation_status == 'pending':
                negotiation.influencer_negotiation_status = 'rejected'
                # Also update the AdRequestNegotiation entry to reflect the influencer's rejection
                negotiation.should_nego_status_change_influencer = False
            else:
                return make_response(jsonify({"message": "Negotiation is not pending for influencer"}), 400)
        
        elif current_user.has_role('sponsor'):
            if negotiation.sponsor_negotiation_status == 'pending':
                negotiation.sponsor_negotiation_status = 'rejected'
                # Also update the AdRequestNegotiation entry to reflect the sponsor's rejection
                negotiation.should_nego_status_change_sponsor = False
            else:
                return make_response(jsonify({"message": "Negotiation is not pending for sponsor"}), 400)

        # Create or update the UserAdRequest entry
        user_ad_request = UserAdRequest.query.filter_by(
            user_id=current_user.id,
            ad_request_id=ad_request.id
        ).first()

        if user_ad_request:
            user_ad_request.status = 'rejected'
            user_ad_request.response_date = datetime.now()
        else:
            user_ad_request = UserAdRequest(
                user_id=negotiation.created_by,
                ad_request_id=ad_request.id,
                status='rejected',
                response_date=datetime.now()
            )
            db.session.add(user_ad_request)

        # Commit the changes to the database
        db.session.commit()

        return make_response(jsonify({"message": "Negotiation rejected and updated successfully"}), 200)

class InfluencerList(Resource):
    @auth_token_required 
    def get(self):
        
        # Extract the search query from request parameters
        search_query = request.args.get('query', '')

        # Start the query
        query = Influencer.query

        # Apply filters based on the search query
        if search_query:
            query = query.filter(
                (Influencer.name.ilike(f'%{search_query}%')) |
                (Influencer.category.ilike(f'%{search_query}%')) |
                (Influencer.reach.ilike(f'%{search_query}%')) |
                (Influencer.niche.ilike(f'%{search_query}%'))
            )

        # Execute the query
        influencers = query.all()

        # Serialize the results
        data = [inf.serialize() for inf in influencers]

        # Return the response
        if not data:
            return make_response(jsonify({"message": "No influencers found", "data": []}))

        return make_response(jsonify({"message": "Got influencer list", "data": data}))
    


    

    

   
        



