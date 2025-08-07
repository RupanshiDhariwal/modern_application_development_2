from flask import Flask, request, jsonify
from flask_security import Security, current_user, verify_password, auth_token_required, roles_accepted


from models import db, user_datastore, User



def make_celery(app):
    from celery import Celery
    celery=Celery(app.import_name)
    import celeryconfig
    celery.config_from_object(celeryconfig)
    return celery

def create_app():
    app = Flask(__name__)
    from config import ConfigDevelopment
    app.config.from_object(ConfigDevelopment)
    db.init_app(app)
    security = Security(app, user_datastore)

   

    # with app.app_context():

    #     db.drop_all()

    #     db.create_all()

    #     user_datastore.find_or_create_role(name='admin',description='Administrator')
    #     user_datastore.find_or_create_role(name='sponsor',description='Sponsor')
    #     user_datastore.find_or_create_role(name='influencer',description='influencer')

    #     db.session.commit()

    #     admin_user = user_datastore.find_user(email="admin@mail.com")

    #     if not admin_user:
    #         User_admin = user_datastore.create_user(email="admin@mail.com", password="admin")
    #         user_datastore.add_role_to_user(User_admin, 'admin')
        
    #     db.session.commit()

    from flask_restful import Api
    api = Api(app, prefix='/api')

    from flask_cors import CORS
    CORS(app)


    from caching import cache
    cache.init_app(app)

    celery_init = make_celery(app)

    from mailer import mail
    mail.init_app(app)

    return app, api, celery_init

app, api_route_handler, celery_app = create_app()
import tasks

from celery.schedules import crontab
celery_app.conf.beat_schedule = {
    'sum-test':{
        'task': 'tasks.sum',
        'schedule': crontab(minute=47, hour=23)
    },
    'email-test':{
        'task': 'tasks.test_mail',
        'schedule': crontab(minute=0, hour=18)
    },
    'send_monthly_report':{
        'task': 'tasks.send_monthly_report',
        'schedule': crontab(minute=0, hour=18, day_of_month=1)
    }
}


@app.route('/celery', methods=['GET'])
def test_celery():
    # job = tasks.sum.delay()
    job = tasks.test_db.delay()
    while not job.ready():
        pass
    return jsonify({"message":"Celery task called", "id": job.id, "status": job.status, "result": job.get()})


@auth_token_required
@app.route('/export_campaigns', methods=['POST'])
def export_campaigns():
    print(current_user.id)
    print(current_user)
    sponsor_id = current_user.id  
    user_email = current_user.email

    if not sponsor_id or not user_email:
        return jsonify({'error': 'User information is missing'}), 400

    # Enqueue the Celery task with the parameters
    tasks.export_campaign_csv.delay(sponsor_id, user_email)

    return jsonify({'message': 'Export process started. You will receive an email once done.'}), 202


from routes.auth import signup, login
api_route_handler.add_resource(signup, '/register')
api_route_handler.add_resource(login, '/login')

from routes.admin import activateSponsor, activeUser, AllUsers,DeactivateUser, DeactivatedSponsors
api_route_handler.add_resource(activateSponsor, '/activate/<int:id>')
api_route_handler.add_resource(activeUser,'/activeUser')
api_route_handler.add_resource(DeactivatedSponsors,'/deactiveted/sponsors')
api_route_handler.add_resource(DeactivateUser,'/deactiveUser/<int:id>')
api_route_handler.add_resource(AllUsers,'/user/all')

from routes.campaign import Campaigns, CampaignSpecific, UserSpecificCampaignList, InfluencerSearchCampaigns, AllCampaigns
api_route_handler.add_resource(Campaigns,'/campaign/')
api_route_handler.add_resource(AllCampaigns,'/campaign/all')
api_route_handler.add_resource(UserSpecificCampaignList,'/campaign/user/specific/')
api_route_handler.add_resource(InfluencerSearchCampaigns,'/campaign/influ/search/')
api_route_handler.add_resource(CampaignSpecific, '/campaign/<int:id>')

from routes.adRequest import AdRequests,AdResquestSpecific,AddNewNegotiation,GetNegotiation,AllAdRequests,GetSponsorNegotiation
api_route_handler.add_resource(AdRequests,'/adrequest')
api_route_handler.add_resource(AllAdRequests,'/adrequest/all')
api_route_handler.add_resource(AdResquestSpecific,'/adrequest/<int:id>')
api_route_handler.add_resource(GetNegotiation,'/adrequest/get/user/negotiation')
api_route_handler.add_resource(GetSponsorNegotiation,'/adrequest/get/sponsor/negotiation')
api_route_handler.add_resource(AddNewNegotiation,'/adrequest/add/negotiation/<int:id>')

from routes.influencer import AcceptRequest, RejectRequest, Influencers, InfluencerSpecific, InfluencerList
api_route_handler.add_resource(Influencers,'/influencer/profile')
api_route_handler.add_resource(InfluencerList,'/influencer/search/list')
api_route_handler.add_resource(InfluencerSpecific,'/influencer/profile/<int:id>')
api_route_handler.add_resource(AcceptRequest,'/adrequest/accept/<int:id>')
api_route_handler.add_resource(RejectRequest,'/adrequest/reject/<int:id>')

from routes.Sponsor import Sponsors, SponsorSpecific, ExportCampaigns
api_route_handler.add_resource(Sponsors,'/sponsor/profile')
api_route_handler.add_resource(ExportCampaigns,'/sponsor/exportcsv')
api_route_handler.add_resource(SponsorSpecific,'/sponsor/profile/<int:id>')


# @app.route('/api/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     email1 = data.get('email')
#     password1 = data.get('password')
#     role1 = data.get('role')
#     user = user_datastore.find_user(email=email1)
#     if not user:
#         user = user_datastore.create_user(email=email1, password=password1)
#         if role1 == "sponsor":
#             # user.active = False
#             user_datastore.add_role_to_user(user, "sponsor")
#             user_datastore.deactivate_user(user)
#         elif role1 == "influencer":
#             user_datastore.add_role_to_user(user, 'influencer')
#         db.session.commit()
#         return jsonify({"message":"User registered successfully"})
#     return jsonify({"message":"User already exists"})


# @app.route('/api/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     email1 = data.get('email')
#     password1 = data.get('password')
#     user = user_datastore.find_user(email=email1)
#     if user:
#         if verify_password(password1, user.password):
#             return jsonify({"message":"Login successful", "authToken": user.get_auth_token()})



# @app.route('/api/test', methods=['POST'])
# @auth_token_required
# @roles_accepted('admin', 'customer')
# def test():
#     return jsonify({"message":"Test successful", "id": current_user.id})
    

# @app.route('/api/activate', methods=['POST'])
# @auth_token_required
# @roles_accepted('admin')
# def activate_manager():
#     data = request.get_json()
#     id = data.get('id')
#     user = user_datastore.find_user(id=id)
#     if user and user.has_role('manager'):
#         user_datastore.activate_user(user)
#         db.session.commit()
#         return jsonify({"message":"User activated successfully"})
#     return jsonify({"message":"User not found"})


# @app.route('/hello_world', methods=['GET'])
# def hello_world():
#     return jsonify({"message":"Hello World"})


if __name__ == "__main__":
    app.run(debug=True)