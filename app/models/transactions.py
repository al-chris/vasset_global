from sqlalchemy.orm import backref
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db
from config import Config
from enum import Enum

from ..models import Media
from ..models.role import Role, RoleNames


class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    wallet_address = db.Column(db.String(120), nullable=False)
    wallet_type = db.Column(db.String(50))
    coin_type = db.Column(db.String(50))
    screenshot_url = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    status = db.Column(db.String(50), default='pending')  # 'pending', 'verified', 'cancelled'
    user_id = db.Column(db.Integer, db.ForeignKey('vasset_user.id'), nullable=False)

    def __repr__(self):
        return f'<id: {self.id}, amount: {self.amount}, created_at: {self.created_at}, user_id: {self.user_id}>'
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
    
    def to_json(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'wallet_address': self.wallet_address,
            'wallet_type': self.wallet_type,
            'coin_type': self.coin_type,
            'screenshot_url': self.screenshot_url,
            'created_at': self.created_at,
            'status': self.status,
            'user_id': self.user_id
        }

