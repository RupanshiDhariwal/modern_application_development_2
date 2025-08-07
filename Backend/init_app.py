from app import create_app
from flask_login import LoginManager, login_user

app, _, _ = create_app()

with app.app_context():
    from models import db, user_datastore
    
    print('inside this')
    db.drop_all()

    db.create_all()

    user_datastore.find_or_create_role(name='admin',description='Administrator')
    user_datastore.find_or_create_role(name='sponsor',description='Sponsor')
    user_datastore.find_or_create_role(name='customer',description='Customer')

    db.session.commit()

    admin_user = user_datastore.find_user(email="admin@mail.com")

    if not admin_user:
        User_admin = user_datastore.create_user(email="admin@mail.com", password="admin")
        user_datastore.add_role_to_user(User_admin, 'admin')
    
    db.session.commit()
    