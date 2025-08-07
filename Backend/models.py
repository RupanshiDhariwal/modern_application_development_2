from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin, AsaList, SQLAlchemyUserDatastore
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey, Enum, JSON
from datetime import datetime

db = SQLAlchemy()




class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(MutableList.as_mutable(AsaList()), nullable=True)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(64), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users', backref=backref('users', lazy='dynamic'))
    # Many-to-many relationship with AdRequest through 'user_ad_request' association table
    ad_requests = relationship('Ad_request', secondary='user_ad_request', back_populates='users')

    # One-to-many relationship with UserAdRequest
    ad_requests_association = relationship('UserAdRequest', back_populates='user')

    # One-to-one relationship with Influencer
    influencer = db.relationship('Influencer', uselist=False, back_populates='user')
    
    # One-to-one relationship with Sponsor
    sponsor = db.relationship('Sponsor', uselist=False, back_populates='user')

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'last_login_at': self.last_login_at,
            'current_login_at': self.current_login_at,
            'last_login_ip': self.last_login_ip,
            'current_login_ip': self.current_login_ip,
            'login_count': self.login_count,
            'active': self.active,
            'confirmed_at': self.confirmed_at,
            'roles': [role.name for role in self.roles],
            'influencer': self.influencer.serialize() if self.influencer else None,
            'sponsor': self.sponsor.serialize() if self.sponsor else None,
            'ad_requests': [ad_request.serialize() for ad_request in self.ad_requests_association]
        }

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

class Influencer(db.Model):
    __tablename__ = 'influencer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    category = db.Column(db.String(255))
    niche = db.Column(db.String(255))
    reach = db.Column(db.Float)  # Reach calculated based on followers/activity

    # Foreign key to link influencer to user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='influencer')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'niche': self.niche,
            'reach': self.reach,
            'user_id':self.user_id
        }

class Sponsor(db.Model):
    __tablename__ = 'sponsor'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255))  # For company sponsors
    individual_name = db.Column(db.String(255))  # For individual sponsors
    industry = db.Column(db.String(255))
    budget = db.Column(db.Float)

    # Foreign key to link sponsor to user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='sponsor')

    def serialize(self):
        return {
            'id': self.id,
            'company_name': self.company_name,
            'individual_name': self.individual_name,
            'industry': self.industry,
            'budget': self.budget
        }




class Campaign(db.Model):
    __tablename__ = 'campaign'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    budget = db.Column(db.Float)
    category = db.Column(db.String(255))
    status = db.Column(Enum('active', 'inactive', 'deleted', name='status_enum'),
                       default='active',
                       nullable=False)
    created_by = db.Column(db.String(255), db.ForeignKey('user.id'))
    updated_by = db.Column(db.String(255), db.ForeignKey('user.id'), default=None)
    created_at = db.Column(db.DateTime, default=datetime.now())
    update_at = db.Column(db.DateTime, default=datetime.now())
    visibility = db.Column(
        Enum('public', 'private', name='visibility_enum'),
        default='public',
        nullable=False
    )
    goals = db.Column(JSON)
    ad_requests = db.relationship('Ad_request', back_populates='campaign', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'category': self.category,
            'budget': self.budget,
            'status': self.status,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'created_at': self.created_at,
            'update_at': self.update_at,
            'visibility': self.visibility,
            'goals': self.goals,
            'ad_requests': [ad_request.serialize() for ad_request in self.ad_requests] if self.ad_requests else []
        }
    


class UserAdRequest(db.Model):
    __tablename__ = 'user_ad_request'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    ad_request_id = Column(Integer, ForeignKey('ad_request.id'))
    status = Column(Enum('accepted', 'rejected','negotiation', name='ad_request_status_enum'), nullable=False)
    response_date = Column(DateTime, default=datetime.now)

    # Relationships to User and AdRequest
    user = relationship('User', back_populates='ad_requests_association')
    ad_request = relationship('Ad_request', back_populates='user_associations')

class Ad_request(db.Model):
    __tablename__ = 'ad_request'
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column('campaign_id', db.Integer(), db.ForeignKey('campaign.id'))
    influencer_id = db.Column('influencer_id', db.Integer(), db.ForeignKey('user.id'))
    messages = db.Column(db.Text)
    requirements = db.Column(db.Text)
    payment_amount = db.Column(db.Float)
    created_by = db.Column(db.String(255), db.ForeignKey('user.id'))
    updated_by = db.Column(db.String(255), db.ForeignKey('user.id'), default=None)
    created_at = db.Column(db.DateTime, default=datetime.now())
    update_at = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(
        Enum('pending', 'accepted', 'rejected', 'deleted', name='status_enum'),
        default='pending',
        nullable=False
    )
    # Relationships to Campaign and User
    campaign = relationship('Campaign', back_populates='ad_requests')
    users = relationship('User', secondary='user_ad_request', back_populates='ad_requests')

    # Relationship to UserAdRequest
    user_associations = relationship('UserAdRequest', back_populates='ad_request')

    def serialize(self):
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'influencer_id': self.influencer_id,
            'messages': self.messages,
            'requirements': self.requirements,
            'payment_amount': self.payment_amount,
            'status': self.status,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'created_at': self.created_at,
            'update_at': self.update_at,
            'campaign': self.campaign.name if self.campaign else None
        }

class AdRequestNegotiation(db.Model):
    __tablename__ = 'ad_request_negotiation'
    id = db.Column(db.Integer, primary_key=True)
    ad_request_id = db.Column(db.Integer, db.ForeignKey('ad_request.id'))
    message = db.Column(db.Text)
    payment_amount = db.Column(db.Float)
    influencer_negotiation_payment_amt = db.Column(db.Float, default=0.0)
    sponsor_negotiation_payment_amt = db.Column(db.Float, default=0.0)
    should_nego_status_change_influencer = db.Column(db.Boolean, default=False)
    should_nego_status_change_sponsor = db.Column(db.Boolean, default=False)
    negotiation_count_influencer = db.Column(db.Integer, default=0)
    negotiation_count_sponsor = db.Column(db.Integer, default=0)
    influencer_negotiation_status = db.Column(
        Enum('pending', 'accepted', 'rejected', name='status_enum'),
        default='pending',
        nullable=False
    )
    sponsor_negotiation_status = db.Column(
        Enum('pending', 'accepted', 'rejected', name='status_enum'),
        default='pending',
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.now())
    created_by = db.Column(db.String(255), db.ForeignKey('user.id'), default=None)
    updated_by = db.Column(db.String(255), db.ForeignKey('user.id'), default=None)
    updated_at = db.Column(db.DateTime, default=datetime.now())
    negotiator_role = db.Column(db.String) 

    def serialize(self):
        return {
            'id': self.id,
            'ad_request_id': self.ad_request_id,
            'message': self.message,
            'payment_amount': self.payment_amount,
            'influencer_negotiation_payment_amt': self.influencer_negotiation_payment_amt,
            'sponsor_negotiation_payment_amt': self.sponsor_negotiation_payment_amt,
            'should_nego_status_change_influencer': self.should_nego_status_change_influencer,
            'should_nego_status_change_sponsor': self.should_nego_status_change_sponsor,
            'negotiation_count_influencer': self.negotiation_count_influencer,
            'negotiation_count_sponsor': self.negotiation_count_sponsor,
            'influencer_negotiation_status': self.influencer_negotiation_status,
            'sponsor_negotiation_status': self.sponsor_negotiation_status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'negotiator_role': self.negotiator_role
        }
