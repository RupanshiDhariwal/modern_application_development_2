from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import current_user
from datetime import datetime
from flask_security import roles_accepted, auth_token_required
from sqlalchemy.orm import aliased

from models import db, Ad_request,AdRequestNegotiation,UserAdRequest

class AdRequests(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def post(self):
        data = request.get_json()
        print('data',data)
        print('current_user',current_user.id)
        campaign_id = data.get('campaign_id')
        influencer_id = data.get('influencer_id')
        messages = data.get('messages')
        requirements = data.get('requirements')
        payment_amount = data.get('payment_amount')

        if not (campaign_id  and messages and requirements and payment_amount):
            return make_response(jsonify({"message":"please fill all required fields"}), 403)


        
        new_request = Ad_request(
                campaign_id=campaign_id,
                influencer_id=influencer_id,
                messages=messages,
                requirements=requirements,
                payment_amount=payment_amount,
                created_by = current_user.id,
                )
        db.session.add(new_request)
        db.session.commit()
        return make_response(jsonify({
                "message":"ad_request sent successfully"  
        }),201)
    
    @auth_token_required
    @roles_accepted('admin','sponsor','influencer')
    def get(self):
        current_user_id = current_user.id  # Assuming you pass the current user ID as a query parameter

        # Query all ad_requests excluding those with status 'deleted'
        ad_requests = Ad_request.query.filter(Ad_request.status != 'deleted').all()

        # Filter ad_requests that do not have an entry in UserAdRequest for the current user
        filtered_ad_requests = []
        for ad_request in ad_requests:
            user_ad_request = UserAdRequest.query.filter_by(ad_request_id=ad_request.id, user_id=current_user_id).first()
            if not user_ad_request:
                filtered_ad_requests.append(ad_request)

        # Serialize the results
        ad_requests_serialized = [ad_request.serialize() for ad_request in filtered_ad_requests]

        return make_response(jsonify({"message":"please fill all required fields","data":ad_requests_serialized}), 200)
    
    

class AdResquestSpecific(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def put(self,id):
        ad_request = Ad_request.query.filter_by(id=id).first()

        if not ad_request:
            return make_response(jsonify({"message":"ad_request not found with this id"}),404)
        
        data = request.get_json()
        campaign_id = data.get('campaign_id')
        influencer_id = data.get('influencer_id')
        messages = data.get('messages')
        requirements = data.get('requirements')
        payment_amount = data.get('payment_amount')
        
        if not (campaign_id  and messages and requirements and payment_amount):
            return make_response(jsonify({"message":"please fill all required fields"}), 403)
        
        ad_request.campaign_id = campaign_id
        ad_request.influencer_id = influencer_id
        ad_request.messages = messages
        ad_request.requirements = requirements
        ad_request.payment_amount = payment_amount
        ad_request.updated_by = current_user.id
        ad_request.updated_at = datetime.now()

        db.session.commit()
        
        return make_response(jsonify({"message":"ad_request updated successfully"}), 200)
    

    @auth_token_required
    @roles_accepted('admin','sponsor','influencer')
    def get(self, id):
        ad_request = Ad_request.query.filter_by(id=id).first()
        ad_req = ad_request.serialize()

        if not ad_request:
            return make_response(jsonify({"message":"No ad_request found with this id"}),404)
        
        return make_response(jsonify({"message":"get specific ad_request", "data":ad_req}), 200)
        

    @auth_token_required
    @roles_accepted('sponsor','admin')
    def delete(self, id):
        ad_request = Ad_request.query.filter_by(id=id).first()
        if not ad_request:
            return make_response(jsonify({"message":"No ad_request found"}), 404)
        ad_request.status = 'deleted'
        db.session.commit()
        return make_response(jsonify({"message":"delete specific ad_request"}),201)
    

class AddNewNegotiation(Resource):
    @auth_token_required
    @roles_accepted('influencer')
    def post(self, id):
        # Fetch the AdRequest
        ad_request = Ad_request.query.filter_by(id=id).first()

        if not ad_request:
            return make_response(jsonify({"message": "ad_request not found with this id"}), 404)

        # Get data from request
        data = request.get_json()
        new_payment_amt = data.get('amount')
        message = data.get('message', '')  # Optional message in negotiation

        # Check if the current user is an influencer
        if current_user.has_role('influencer'):
            negotiator_role = 'influencer'
        else:
            return make_response(jsonify({"message": "Only influencers can initiate negotiations"}), 403)

        # Create a new AdRequestNegotiation entry
        negotiation = AdRequestNegotiation(
            ad_request_id=ad_request.id,
            message=message,
            payment_amount=ad_request.payment_amount,
            influencer_negotiation_payment_amt=new_payment_amt,  # Set new payment amount
            sponsor_negotiation_payment_amt=0.0,  # Default to 0.0 as this is an influencer's negotiation
            should_nego_status_change_influencer=False,  # Set the flags as True for the influencer's side
            should_nego_status_change_sponsor=True,
            negotiation_count_influencer=1,  # Initialize with 1 for the first negotiation
            negotiation_count_sponsor=0,
            negotiator_role=negotiator_role,
            created_by=current_user.id,
            created_at=datetime.now()
        )

        # Add to the session and commit
        db.session.add(negotiation)
        db.session.commit()

        # Create an entry in UserAdRequest with status 'negotiation'
        user_ad_request = UserAdRequest(
            user_id=current_user.id,
            ad_request_id=ad_request.id,
            status='negotiation',
            response_date=datetime.now()
        )

        # Add to the session and commit
        db.session.add(user_ad_request)
        db.session.commit()

        return make_response(jsonify({"message": "Negotiation request sent successfully"}), 200)
    

#using this API for getting active negotiation of ad requests based on user_id  
class GetNegotiation(Resource):
    @auth_token_required
    @roles_accepted('influencer','sponsor')
    def get(self):

        # Fetch user ad requests with status 'negotiation'
        user_ad_requests = UserAdRequest.query.filter_by(user_id=current_user.id, status='negotiation').all()

        # Prepare response
        negotiations = []
        for user_ad_request in user_ad_requests:
            ad_request = Ad_request.query.get(user_ad_request.ad_request_id)
            if ad_request:
                ad_request_info = ad_request.serialize()
                ad_request_negotiations = AdRequestNegotiation.query.filter_by(ad_request_id=ad_request.id).all()
                negotiations.append({
                    'ad_request': ad_request_info,
                    'negotiations': [negotiation.serialize() for negotiation in ad_request_negotiations]
                })

        return jsonify(negotiations)
    

class GetSponsorNegotiation(Resource):
    @auth_token_required
    def get(self):

        # Fetch user ad requests with status 'negotiation'
        user_ad_requests = Ad_request.query.filter_by(created_by=current_user.id).all()

        # Prepare response
        negotiations = []
        for user_ad_request in user_ad_requests:
            ad_request = Ad_request.query.get(user_ad_request.id)
            if ad_request:
                ad_request_info = ad_request.serialize()
                ad_request_negotiations = AdRequestNegotiation.query.filter_by(ad_request_id=ad_request.id).all()
                negotiations.append({
                    'ad_request': ad_request_info,
                    'negotiations': [negotiation.serialize() for negotiation in ad_request_negotiations]
                })

        return jsonify(negotiations)
    
    

    

class EditOldNegotiate(Resource):
    @auth_token_required
    @roles_accepted('sponsor', 'influencer')
    def put(self, id):
        ad_request = Ad_request.query.filter_by(id=id).first()

        if not ad_request:
            return make_response(jsonify({"message": "ad_request not found with this id"}), 404)

        data = request.get_json()
        new_payment_amt = data.get('amount')
        message = data.get('message', '')  # Optional message in negotiation

        if current_user.has_role('influencer'):
            negotiator_role = 'influencer'
            new_influencer_amount = new_payment_amt
            new_sponsor_amount = ad_request.sponsor_negotiation_payment_amt
            should_nego_status_change_influencer = False
            should_nego_status_change_sponsor = True
            negotiation_count_influencer = ad_request.negotiation_count_influencer + 1
            negotiation_count_sponsor = ad_request.negotiation_count_sponsor

        elif current_user.has_role('sponsor'):
            negotiator_role = 'sponsor'
            new_influencer_amount = ad_request.influencer_negotiation_payment_amt
            new_sponsor_amount = new_payment_amt
            should_nego_status_change_influencer = True
            should_nego_status_change_sponsor = False
            negotiation_count_influencer = ad_request.negotiation_count_influencer
            negotiation_count_sponsor = ad_request.negotiation_count_sponsor + 1

        # Create a new AdRequestNegotiation entry
        negotiation = AdRequestNegotiation(
            ad_request_id=ad_request.id,
            message=message,
            payment_amount=new_payment_amt,
            influencer_negotiation_payment_amt=new_influencer_amount,
            sponsor_negotiation_payment_amt=new_sponsor_amount,
            should_nego_status_change_influencer=should_nego_status_change_influencer,
            should_nego_status_change_sponsor=should_nego_status_change_sponsor,
            negotiation_count_influencer=negotiation_count_influencer,
            negotiation_count_sponsor=negotiation_count_sponsor,
            negotiator_role=negotiator_role,
            created_at=datetime.now()
        )

        # Add to the session and commit
        db.session.add(negotiation)
        db.session.commit()

        return make_response(jsonify({"message": "Negotiate request sent successfully"}), 200)
    
class AllAdRequests(Resource):
    from caching import cache
    @auth_token_required
    @roles_accepted('admin')
    @cache.cached(timeout=30)
    def get(self):
        ad_requests = Ad_request.query.all()
        data = [ad_request.serialize() for ad_request in ad_requests]
        return make_response(jsonify({"message": "Got ad request list", "data": data}), 200)

        



