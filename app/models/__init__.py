'''
This package contains the database models for the Flask application.

It includes models for User Transaction, Role, etc. Each model corresponds to a table in the database.

@author Chris
@link: https://github.com/al-chris
@package vasset_global
'''

from .role import Role, RoleNames
from .user import User, TempUser
from .media import Media