from applications.database import db
from datetime import datetime


class Role(db.Model):
    __tablename__ = 'role'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Admin(db.Model):
    __tablename__ ="admin"
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    admin_name = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    email = db.Column(db.String(255), unique=True)
        

    def to_json(self) :
        return {
            "id":self.id, 
            "admin_name":self.admin_name, 
            "password":self.password, 
            "email":self.email
        }
    

class User(db.Model):
    __tablename__ ="user"
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    username = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    email = db.Column(db.String(255), unique=True)
        

    def to_json(self) :
        return {
            "id":self.id, 
            "username":self.username, 
            "password":self.password, 
            "email":self.email
        }
        




class Sponsor(db.Model):
    __tablename__ = 'sponsor'
    sponsor_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    company_name = db.Column(db.String(255))
    industry = db.Column(db.String(255))
    budget = db.Column(db.Float)
    user = db.relationship('User', backref=db.backref('sponsor_profile', uselist=False))
    campaigns = db.relationship('Campaign', backref='sponsor', lazy='dynamic')
    ads = db.relationship('Ad', backref='sponsor', lazy='dynamic')

    @property
    def sponsor_name(self):
        return self.user.username if self.user else "Unknown"

    @property
    def sponsor_email(self):
        return self.user.email if self.user else "Unknown"

    def to_json(self) :
        return {
            'sponsor_id': self.sponsor_id,
            'sponsor_name': self.sponsor_name,
            'sponsor_email': self.sponsor_email,
            'company_name': self.company_name,
            'industry': self.industry,
            'budget': self.budget,
            'user': self.user.to_json() if self.user else None,
            'campaigns': [campaign.to_json() for campaign in self.campaigns],
            'ads': [ad.to_json() for ad in self.ads]
        }
        



class Influencer(db.Model):
    __tablename__ = 'influencer'
    influencer_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    category = db.Column(db.String(255))
    niche = db.Column(db.String(255))
    reach = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('influencer_profile', uselist=False))
    ad_requests = db.relationship('AdRequest', backref='influencer', lazy='dynamic')


    @property
    def influencer_name(self):
        return self.user.username
    
    @property
    def influencer_email(self):
        return self.user.email
    
    def to_json(self):
        return {
                'influencer_id': self.influencer_id,
                'influencer_name': self.influencer_name,
                'influencer_email': self.influencer_email,
                'category': self.category,
                'niche': self.niche,
                'reach': self.reach,
                'user': self.user.to_json() if self.user else None,
                'ad_requests': [ad_request.to_json() for ad_request in self.ad_requests]
            }
    

    




class Campaign(db.Model):
    __tablename__ = 'campaign'
    campaign_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    campaign_name = db.Column(db.String(255))
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.sponsor_id'))
    description = db.Column(db.Text)
    start_date = db.Column(db.Text)
    end_date = db.Column(db.Text)
    budget = db.Column(db.Float)
    visibility = db.Column(db.String(255))
    goals = db.Column(db.String(255))
    ads = db.relationship('Ad', backref='campaign', lazy='dynamic')

    def to_json(self):
        return {
            'campaign_id': self.campaign_id,
            'campaign_name': self.campaign_name,
            'sponsor_id': self.sponsor_id,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'budget': self.budget,
            'visibility': self.visibility,
            'goals': self.goals,
            'ads': [ad.to_json() for ad in self.ads]
    }

    


class Ad(db.Model):
    __tablename__ = 'ad'
    ad_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ad_name = db.Column(db.String(255))
    content = db.Column(db.Text)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.campaign_id'))
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.sponsor_id'))
    start_date = db.Column(db.DateTime)
    requirements = db.Column(db.Text)
    budget = db.Column(db.Float)
    status = db.Column(db.String(255))
    target_audience = db.Column(db.String(255))
    ad_requests = db.relationship('AdRequest', backref='ad', lazy='dynamic')

    def to_json(self):
        return {
            'ad_id': self.ad_id,
            'ad_name': self.ad_name,
            'content': self.content,
            'campaign_id': self.campaign_id,
            'sponsor_id': self.sponsor_id,
            'start_date': self.start_date,
            'requirements': self.requirements,
            'budget': self.budget,
            'status': self.status,
            'target_audience': self.target_audience,
        }


class AdRequest(db.Model):
    __tablename__ = 'ad_request'
    ad_request_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    ad_id = db.Column(db.Integer, db.ForeignKey('ad.ad_id'))
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.sponsor_id'))
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.influencer_id'))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    message = db.Column(db.Text)
    status = db.Column(db.String(255))
    requirements = db.Column(db.Text)
    payment = db.Column(db.Float)


    def to_json(self):
        return {
            'ad_request_id': self.ad_request_id,
            'ad_id': self.ad_id,
            'sponsor_id': self.sponsor_id,
            'influencer_id': self.influencer_id,
            'campaign_id': self.campaign_id,
            'message': self.message,
            'status': self.status,
            'requirements': self.requirements,
            'payment': self.payment
    }