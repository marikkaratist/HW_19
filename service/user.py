import hashlib
import base64
import hmac

import constants
from dao.model.user import User
from dao.user import UserDAO
from setup_db import db


class UserService:
    def __init__(self, dao: UserDAO):
        self.session = db.session
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def get_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def create(self, user_d: dict) -> dict:
        user_d['password'] = self.generate_password(user_d['password'])
        return self.dao.create(user_d)

    def update(self, user_d):
        user_d['password'] = self.generate_password(user_d['password'])
        return self.dao.update(user_d)

    def delete(self, uid):
        self.dao.delete(uid)

    def generate_password(self, password: str) -> str:
        hashed_password: bytes = hashlib.pbkdf2_hmac(
            hash_name=constants.HASH_NAME,
            salt=constants.HASH_SALT.encode('utf-8'),
            iterations=constants.HASH_GEN_ITERATIONS,
            password=password.encode('utf-8'),
        )
        return base64.b64encode(hashed_password).decode('utf-8')

    def compare_passwords(self, password_hash, other_password) -> bool:
        decoded_digest = base64.b64decode(password_hash)
        hashed_password: bytes = hashlib.pbkdf2_hmac(
            hash_name=constants.HASH_NAME,
            salt=constants.HASH_SALT.encode('utf-8'),
            iterations=constants.HASH_GEN_ITERATIONS,
            password=other_password.encode('utf-8'),
        )
        return hmac.compare_digest(decoded_digest, hashed_password)
