from sqlalchemy.orm import backref
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db
from config import Config
from enum import Enum

from app.models import Media, Role, RoleNames

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
    _password = db.Column(db.String(128))
    email_verified = db.Column(db.Boolean, default=False)
    phone_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.UTC), onupdate=datetime.now(timezone.UTC))

    # Relationships
    profile = db.relationship('Profile', back_populates="vasset_user", uselist=False, cascade="all, delete-orphan")
    address = db.relationship('Address', back_populates="vasset_user", uselist=False, cascade="all, delete-orphan")
    identification = db.relationship('Identification', back_populates="vasset_user", uselist=False, cascade="all, delete-orphan")
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'), cascade="all, delete-orphan", single_parent=True)
    nextofkin = db.relationship('NextOfKin', back_populates="vasset_user", uselist=False, cascade="all, delete-orphan")
    # user_settings = db.relationship('UserSettings', back_populates='vasset_user', uselist=False, cascade='all, delete-orphan')


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)
    
    def verify_password(self, password):
        '''
        #This returns True if the password is same as hashed password in the database.
        '''
        return check_password_hash(self._password, password)
    
    @property
    def role_names(self) -> list[str]:
        """Returns a list of role names for the user."""
        return [str(role.name.value) for role in self.roles]

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
        
        address_info = {}
        if self.address:
            address_info.update({
                'country': self.address.country,
                'state': self.address.state,
                'city': self.address.city,
                'address': self.address.address,
                'postal_code': self.address.postal_code
            })
        
        profile_data = {}
        if self.profile:
            profile_data.update({
                'firstname': self.profile.firstname,
                'lastname': self.profile.lastname,
                'gender': self.profile.gender,
                'phone': self.profile.phone,
                'birthday': self.profile.birthday,
                'profile_picture': self.profile.profile_pic,
                'currency_code': self.address.currency_code
            })

        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            **address_info,
            **profile_data
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
    currency_code = db.Column(db.String(50), nullable=True)
    _bvn = db.Column(db.Integer(), unique=True)
    
    vasset_user_id = db.Column(db.Integer, db.ForeignKey('vasset_user.id', ondelete='CASCADE'), nullable=False,)
    vasset_user = db.relationship('User', back_populates="profile")
    
    def __repr__(self):
        return f'<profile ID: {self.id}, name: {self.firstname}>'
    
    @property
    def bvn(self):
        return self._bvn
    
    @bvn.setter
    def bvn(self, value):
        self._bvn = int(value)
    
    # @property
    # def referral_link(self):
    #     return f'{Config.DOMAIN_NAME}/signup/{self.trendit3_user.username}'
    
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
            'profile_picture': self.profile_pic
        }


class Address(db.Model):
    __tablename__ = "address"
    
    id = db.Column(db.Integer(), primary_key=True)
    country = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(150), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(100), nullable=True)
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
    issue_date = db.Column(db.Date, nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    picture_id = db.Column(db.Integer(), db.ForeignKey('media.id'), nullable=False)
    
    vasset_user_id = db.Column(db.Integer, db.ForeignKey('vasset_user.id', ondelete='CASCADE'), nullable=False,)
    vasset_user = db.relationship('User', back_populates="identification")
    
    def __repr__(self):
        return f'<address ID: {self.id}, country: {self.country}, LGA: {self.local_government}, person ID: {self.vasset_user_id}>'
    
    @property
    def id_image(self):
        if self.picture_id:
            theImage = Media.query.get(self.picture_id)
            if theImage:
                return theImage.get_path()
            else:
                return ''
        else:
            return ''
        
    @staticmethod
    def get_id_type_from_string(id: str):
        id_map = {
            'passport': IdentificationType.PASSPORT,
            'nin': IdentificationType.NIN,
            'drivers licence': IdentificationType.DRIVERS_LICENCE,
            'national id': IdentificationType.NATIONAL_ID
        }

        return id_map.get(id.lower())

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


class NextOfKin(db.Model):
    id = db.Column(db.Integer(), unique=True, primary_key=True)
    relationship = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(200), nullable=True)
    lastname = db.Column(db.String(200), nullable=True)
    gender = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(50), unique=True)
    address = db.Column(db.String(150), nullable=True)
    
    vasset_user_id = db.Column(db.Integer, db.ForeignKey('vasset_user.id', ondelete='CASCADE'), nullable=False,)
    vasset_user = db.relationship('User', back_populates="nextofkin")
    
    def __repr__(self):
        return f'<D: {self.id}, name: {self.firstname}, email: {self.email}>'
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        
    def to_dict(self):
        return {
            'id': self.id,
            'relationship': self.relationship,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'gender': self.gender,
            'phone': self.phone,
            'email': self.email,
            'address': self.address
        }