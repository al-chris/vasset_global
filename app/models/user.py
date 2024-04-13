from sqlalchemy.orm import backref
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db
from config import Config
from enum import Enum

from app.models import Media

class TempUser(db.Model):
    '''
    TempUser model class
    '''
    __tablename__ = 'temp_user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ID: {self.id}, email: {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'date_joined': self.date_joined,
        }    


class User(db.Model):
    '''
    User model class
    '''
    __tablename__ = 'vasset_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.UTC), onupdate=datetime.now(timezone.UTC))

    # Relationships
    profile = db.relationship('Profile', back_populates="vasset_user", uselist=False, cascade="all, delete-orphan")
    address = db.relationship('Address', back_populates="vasset_user", uselist=False, cascade="all, delete-orphan")
    identification = db.relationship('Identification', back_populates="vasset_user", uselist=False, cascade="all, delete-orphan")


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        '''
        #This returns True if the password is same as hashed password in the database.
        '''
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<ID: {self.id}, username: {self.username}, email: {self.email}>'
    
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    

class OneTimeToken(db.Model):
    __tablename__ = "one_time_token"
    
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(), nullable=True, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    used = db.Column(db.Boolean, default=False)

    vasset_user_id = db.Column(db.Integer, db.ForeignKey('trendit3_user.id', ondelete='CASCADE'))
    vasset_user = db.relationship('User', back_populates="otp_token")
    
    def __repr__(self):
        return f'<ID: {self.id}, user ID: {self.vasset_user_id}, code: ******, used: {self.used}>'
    
    @classmethod
    def create_token(cls, token, vasset_user_id):
        token = cls(token=token, vasset_user_id=vasset_user_id)
        
        db.session.add(token)
        db.session.commit()
        return token
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'token': self.token,
            'created_at': self.created_at,
            'used': self.used,
            'user_id': self.vasset_user_id,
        }


class Profile(db.Model):
    __tablename__ = "profile"
    
    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(200), nullable=True)
    lastname = db.Column(db.String(200), nullable=True)
    gender = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(120), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    profile_picture_id = db.Column(db.Integer(), db.ForeignKey('media.id'), nullable=True)
    
    vasset_user_id = db.Column(db.Integer, db.ForeignKey('trendit3_user.id', ondelete='CASCADE'), nullable=False,)
    vasset_user = db.relationship('User', back_populates="profile")
    
    def __repr__(self):
        return f'<profile ID: {self.id}, name: {self.firstname}>'
    
    @property
    def referral_link(self):
        return f'{Config.DOMAIN_NAME}/signup/{self.trendit3_user.username}'
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
    
    @property
    def profile_pic(self):
        if self.profile_picture_id:
            theImage = Media.query.get(self.profile_picture_id)
            if theImage:
                return theImage.get_path()
            else:
                return ''
        else:
            return ''
        
    def to_dict(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'gender': self.gender,
            'phone': self.phone,
            'birthday': self.birthday,
            'profile_picture': self.profile_pic,
            'referral_link': f'{self.referral_link}',
        }


class Address(db.Model):
    __tablename__ = "address"
    
    id = db.Column(db.Integer(), primary_key=True)
    country = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(150), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    currency_code = db.Column(db.String(50), nullable=True)
    postal_code = db.Column(db.String(6), nullable=True)
    
    vasset_user_id = db.Column(db.Integer, db.ForeignKey('vasset_user.id', ondelete='CASCADE'), nullable=False,)
    vasset_user = db.relationship('User', back_populates="address")
    
    def __repr__(self):
        return f'<address ID: {self.id}, country: {self.country}, LGA: {self.local_government}, person ID: {self.vasset_user_id}>'
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'country': self.country,
            'state': self.state,
            'local_government': self.local_government,
            'currency': self.currency_code,
            'user_id': self.vasset_user_id
        }


class IdentificationType(Enum):
    PASSPORT = 'passport'
    NIN = 'nin'
    DRIVERS_LICENCE = 'drivers licence'
    NATIONAL_ID = 'national id'


class Identification(db.Model):
    __tablename__ = "identification"
    
    id = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.Enum(IdentificationType), unique=True, nullable=False)
    issue_date = db.Column(db.DateTime, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    picture = db.Column(db.Integer(), db.ForeignKey('media.id'), nullable=False)
    bvn = db.Column(db.Integer(), unique=True)
    
    vasset_user_id = db.Column(db.Integer, db.ForeignKey('vasset_user.id', ondelete='CASCADE'), nullable=False,)
    vasset_user = db.relationship('User', back_populates="identification")
    
    def __repr__(self):
        return f'<address ID: {self.id}, country: {self.country}, LGA: {self.local_government}, person ID: {self.vasset_user_id}>'
    
    @property
    def bvn(self):
        return self.bvn
    
    @bvn.setter
    def bvn(self, value):
        self.bvn = int(value)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'issue_date': self.issue_date,
            'expiration_date': self.expiration_date,
            'picture': self.picture,
            'bvn': self.bvn,
            'user_id': self.vasset_user_id
        }
