from sqlalchemy.orm import backref
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db
from config import Config
from enum import Enum

from ..models import Media
from ..models.role import Role, RoleNames



class Stock(db.Model):
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('vasset_user.id'), nullable=False)

    def __repr__(self):
        return f'<symbol: {self.symbol}, quantity: {self.quantity}>'
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
    
    def to_json(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'quantity': self.quantity,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    

class RealEstate(db.Model):
    __tablename__ = 'real_estates'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    value = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('vasset_user.id'), nullable=False)

    def __repr__(self):
        return f'<id: {self.id}, address: {self.address}, value: {self.value}>'
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'address': self.address,
            'value': self.value,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Business(db.Model):
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1500))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('vasset_user.id'), nullable=False)

    def __repr__(self):
        return f'<id: {self.id}, name: {self.name}, description: {self.description}>'
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Crypto(db.Model):
    __tablename__ = 'cryptos'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('vasset_user.id'), nullable=False)

    def __repr__(self):
        return f'<symbol: {self.symbol}, amount: {self.amount}>'
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'amount': self.amount,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class NFT(db.Model):
    __tablename__ = 'nfts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    uri = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('vasset_user.id'), nullable=False)

    def __repr__(self):
        return f'<id: {self.id}, name: {self.name}, uri: {self.uri}>'

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'uri': self.uri,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class SocialMedia(db.Model):
    __tablename__ = 'social_media'
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1500))
    proof_pic_id = db.Column(db.Integer(), db.ForeignKey('media.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('vasset_user.id'), nullable=False)

    def __repr__(self):
        return f'<id: {self.id}, platform: {self.platform}, username: {self.username}, description: {self.description}>'
    
    @property
    def proof_pic(self):
        if self.profile_picture_id:
            theImage = Media.query.get(self.profile_picture_id)
            if theImage:
                return theImage.get_path()
            else:
                return ''
        else:
            return ''
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
    
    def to_json(self):
        return {
            'id': self.id,
            'platform': self.platform,
            'username': self.username,
            'description': self.description,
            'proof_pic': self.proof_pic,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }