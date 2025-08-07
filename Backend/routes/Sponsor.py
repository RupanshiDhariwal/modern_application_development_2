from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import current_user, auth_token_required
from models import db, Sponsor
import tasks

class Sponsors(Resource):
    @auth_token_required
    def post(self):
        data = request.get_json()
        print('data', data)
        print('current_user', current_user.id)
        company_name = data.get('company_name')
        individual_name = data.get('individual_name')
        industry = data.get('industry')
        budget = data.get('budget')

        if not (company_name or individual_name):
            return make_response(jsonify({"message": "Company name or individual name is required"}), 403)
        
        sponsor = Sponsor.query.filter_by(company_name=company_name, individual_name=individual_name).first()

        if not sponsor:
            new_sponsor = Sponsor(
                company_name=company_name,
                individual_name=individual_name,
                industry=industry,
                budget=budget,
                user_id=current_user.id
            )
            db.session.add(new_sponsor)
            db.session.commit()
            return make_response(jsonify({
                "message": "Sponsor profile created successfully"
            }), 201)
        return jsonify({
            "message": "A sponsor with this company or individual name already exists"
        })

    @auth_token_required
    def get(self):
        sponsors = Sponsor.query.all()
        data = [sp.serialize() for sp in sponsors]

        if not data:
            return make_response(jsonify({"message": "No sponsors found", "data": []}))

        return make_response(jsonify({"message": "Got sponsor list", "data": data}))


class SponsorSpecific(Resource):
    @auth_token_required
    def put(self, id):
        sponsor = Sponsor.query.filter_by(user_id=id).first()

        if not sponsor:
            return make_response(jsonify({"message": "Sponsor not found with this id"}), 404)

        data = request.get_json()
        company_name = data.get('company_name')
        individual_name = data.get('individual_name')
        industry = data.get('industry')
        budget = data.get('budget')

        if not (company_name or individual_name):
            return make_response(jsonify({"message": "Company name or individual name is required"}), 403)

        sponsor.company_name = company_name
        sponsor.individual_name = individual_name
        sponsor.industry = industry
        sponsor.budget = budget
        db.session.commit()

        return make_response(jsonify({"message": "Sponsor profile updated successfully"}), 200)

    @auth_token_required
    def get(self, id):
        sponsor = Sponsor.query.filter_by(user_id=id).first()
        if not sponsor:
            return make_response(jsonify({"message": "No sponsor found with this id"}), 404)

        return make_response(jsonify({"message": "Got specific sponsor", "data": sponsor.serialize()}), 200)
    

class ExportCampaigns(Resource):
    @auth_token_required
    def post(self):
        # Print for debugging purposes
        print('current_user.id:', current_user.id)
        print('current_user:', current_user)

        sponsor_id = current_user.id
        user_email = current_user.email

        # Check if sponsor_id and user_email are available
        if not sponsor_id or not user_email:
            return make_response(jsonify({'error': 'User information is missing'}), 400)

        # Enqueue the Celery task with the parameters
        tasks.export_campaign_csv.delay(sponsor_id, user_email)

        return make_response(jsonify({'message': 'Export process started. You will receive an email once done.'}), 202)

