from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import current_user
from datetime import datetime
from flask_security import roles_accepted, auth_token_required
from sqlalchemy import or_

from models import db, Campaign

class Campaigns(Resource):
    @auth_token_required
    @roles_accepted('sponsor')
    def post(self):
        data = request.get_json()
        print('data',data)
        print('current_user',current_user.id)
        name = data.get('name')
        description = data.get('description')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        budget = data.get('budget')
        visibility = data.get('visibility')
        goals = data.get('goals')
        category = data.get('category')

        if not (name and description and start_date and end_date and budget and goals):
            return make_response(jsonify({"message":"please fill all required fields"}), 403)


        campaign = Campaign.query.filter_by(name=name).first()
     
        if not campaign:
            new_campaign = Campaign(
                name=name,
                description=description,
                start_date=datetime.strptime(data.get('start_date'), "%Y-%m-%d").date(),
                end_date=datetime.strptime(data.get('end_date'), "%Y-%m-%d").date(),
                created_by = current_user.id,
                category=category,
                budget=budget,
                visibility=visibility,
                goals=goals
                )
            db.session.add(new_campaign)
            db.session.commit()
            return make_response(jsonify({
                "message":"Campaign added successfully"  
            }),201)
        return make_response(jsonify({
            "message":"campaign with this name already exist"
        }),403)
    
    @auth_token_required
    @roles_accepted('admin','sponsor','influencer')
    def get(self):
        campaigns = Campaign.query.filter(Campaign.status != 'deleted').all()
        data = [camp.serialize() for camp in campaigns]

        if not data:
            return make_response(jsonify({"message":"No campaign found","data":[]}))
        
        return make_response(jsonify({"message":"got campaign list", "data": data}))
    


class AllCampaigns(Resource):
    from caching import cache
    @auth_token_required
    @roles_accepted('admin')
    @cache.cached(timeout=30)
    def get(self):
        campaigns = Campaign.query.all()
        
        # Serialize the campaigns
        data = [camp.serialize() for camp in campaigns]
        
        
        status_counts = {
            "active": 0,
            "deleted": 0,
            "inactive": 0
        }
        
        visibility_counts = {
            "public": 0,
            "private": 0
        }
        
        
        for camp in campaigns:
            if camp.status == "active":
                status_counts["active"] += 1
            elif camp.status == "deleted":
                status_counts["deleted"] += 1
            elif camp.status == "inactive":
                status_counts["inactive"] += 1
            
            if camp.visibility == "public":
                visibility_counts["public"] += 1
            elif camp.visibility == "private":
                visibility_counts["private"] += 1
        
        # Create the response
        response = {
            "message": "got campaign list",
            "data": data,
            "status_counts": status_counts,
            "visibility_counts": visibility_counts
        }
        
        return make_response(jsonify(response), 200)
    

class CampaignSpecific(Resource):
    @auth_token_required
    @roles_accepted('sponsor','admin')
    def put(self,id):
        campaign = Campaign.query.filter_by(id=id).first()

        if not campaign:
            return make_response(jsonify({"message":"campaign not found with this id"}),404)
        
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        category = data.get('category')
        budget = data.get('budget')
        visibility = data.get('visibility')
        goals = data.get('goals')
        
        if not (name and description and start_date and end_date and budget and goals):
            return make_response(jsonify({"message":"please fill all required fields"}), 403)
        
        campaign.name = name
        campaign.description = description
        campaign.start_date = datetime.strptime(data.get('start_date'), "%Y-%m-%d").date()
        campaign.end_date = datetime.strptime(data.get('end_date'), "%Y-%m-%d").date()
        campaign.category = category
        campaign.budget = budget
        campaign.visibility = visibility
        campaign.goals = goals
        campaign.updated_by = current_user.id
        campaign.updated_at = datetime.now()

        db.session.commit()
        
        return make_response(jsonify({"message":"campaign updated successfully"}), 200)
    

    @auth_token_required
    @roles_accepted('admin','sponsor','influencer')
    def get(self, id):
        campaign = Campaign.query.filter_by(id=id).first()
        camp = campaign.serialize()

        if not campaign:
            return make_response(jsonify({"message":"No campaign found with this id"}),404)
        
        return make_response(jsonify({"message":"get specific campaign", "data":camp}), 200)
        

    @auth_token_required
    @roles_accepted('sponsor','admin')
    def delete(self, id):
        campaign = Campaign.query.filter_by(id=id).first()
        if not campaign:
            return make_response(jsonify({"message":"No campaign found"}), 404)
        campaign.status = "deleted"
        db.session.commit()
        return make_response(jsonify({"message":"delete specific campaign"}),201)
    


class UserSpecificCampaignList(Resource):
    @auth_token_required
    @roles_accepted('admin', 'sponsor', 'influencer')
    def get(self):
        # Get the current user's ID from the JWT token
        
        user_id = current_user.id # Adjust if user ID is stored differently in your token

        # Extract search query from request parameters
        search_query = request.args.get('query', '')

        # Start the query
        query = Campaign.query.filter(
            Campaign.status != 'deleted',
            Campaign.created_by == user_id
        )

        # Apply search filter if query is provided
        if search_query:
            query = query.filter(Campaign.name.ilike(f'%{search_query}%'))

        # Execute the query
        campaigns = query.all()

        # Serialize the results
        data = [camp.serialize() for camp in campaigns]

        # Return the response
        if not data:
            return make_response(jsonify({"message": "No campaign found", "data": []}))

        return make_response(jsonify({"message": "Got campaign list", "data": data}))


class InfluencerSearchCampaigns(Resource):
    @auth_token_required
    @roles_accepted('admin', 'sponsor', 'influencer')
    def get(self):
        search = request.args.get('search', '').strip()

        # Start the query
        query = Campaign.query.filter(Campaign.status != 'deleted',Campaign.visibility != 'private')

        # Apply filters based on the search parameter
        if search:
            try:
                # Check if the search term is a valid budget number
                search_budget = float(search)
                query = query.filter(Campaign.budget == search_budget)
            except ValueError:
                # If the search term isn't a valid budget number, filter by name or category
                query = query.filter(
                    or_(
                        Campaign.name.ilike(f'%{search}%'),
                        Campaign.category.ilike(f'%{search}%')
                    )
                )

        campaigns = query.all()
        data = [camp.serialize() for camp in campaigns]

        if not data:
            return make_response(jsonify({"message": "No campaign found", "data": []}),200)
        
        return make_response(jsonify({"message": "Got campaign list", "data": data}), 200)

        



