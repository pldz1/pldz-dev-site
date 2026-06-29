import base64
import io
import os
import uuid
import jwt
import pyotp
import qrcode
import qrcode.image.svg
from jwt import PyJWTError
from datetime import datetime, timedelta
from fastapi import Request, HTTPException
from passlib.context import CryptContext
from typing import TypedDict

from core import Logger
from scripts.db.connection import _lock, _read_json, _write_json, get_users_db_path


ALGORITHM = "HS256"

SECRET_KEY = os.getenv("SECRET_KEY")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin@pldz1.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "123")
TWO_FACTOR_ISSUER = os.getenv("TWO_FACTOR_ISSUER", "pldz-dev-site")

ACCESS_EXPIRE = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))
REFRESH_EXPIRE = timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7)))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserItem(TypedDict):
    username: str
    password: str
    raw_password: str
    nickname: str
    avatar: str
    isadmin: bool
    role: str
    token: str
    blacklisted: bool
    two_factor_enabled: bool
    two_factor_secret: str
    two_factor_pending_secret: str


class AuthorizedHandler:

    def __init__(self) -> None:
        pass

    @classmethod
    def init_admin(cls):
        cls.add_user(ADMIN_USERNAME, ADMIN_PASSWORD, "爬楼的猪", "/api/v1/website/image/avatar/admin.jpg")
        Logger.info(f"✔ 初始化管理员账号: {ADMIN_USERNAME}")

    @classmethod
    def create_token(cls, username: str, expires: timedelta, token_type: str):
        payload = {"sub": username, "type": token_type, "exp": datetime.now() + expires}
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return pwd_context.hash(password)

    @classmethod
    def verify_password(cls, password: str, hashed: str) -> bool:
        return pwd_context.verify(password, hashed)

    @classmethod
    def _clean_user(cls, user: dict) -> dict:
        result = dict(user)
        result.pop('password', None)
        result.pop('token', None)
        result.pop('blacklisted', None)
        result.pop('two_factor_secret', None)
        result.pop('two_factor_pending_secret', None)
        result['two_factor_enabled'] = bool(user.get('two_factor_enabled'))
        return result

    @classmethod
    def get_current_user(cls, request: Request):
        token = request.cookies.get('access_token')
        if not token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if data.get('type') != 'access':
                raise HTTPException(status_code=401, detail="Invalid token type")
            username = data.get('sub')
            user = cls.get_user_by_username(username)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except PyJWTError as e:
            Logger.error(f"✖ JWT 错误: {e}")
            raise HTTPException(status_code=401, detail="Invalid or expired token")

    @classmethod
    def check_admin(cls, username: str):
        return username == ADMIN_USERNAME

    @classmethod
    def create_access_token(cls, user):
        return cls.create_token(user, ACCESS_EXPIRE, 'access')

    @classmethod
    def create_refresh_token(cls, user):
        tok = cls.create_token(user, REFRESH_EXPIRE, 'refresh')
        cls.update_user_token(user, tok)
        return tok

    @classmethod
    def blacklist_token(cls, token: str) -> bool:
        db = get_users_db_path()
        with _lock:
            data = _read_json(db)
            for user in data.values():
                if user.get('token') == token:
                    user['blacklisted'] = True
                    _write_json(db, data)
                    return True
        return False

    @classmethod
    def is_token_blacklisted(cls, token: str) -> bool:
        with _lock:
            data = _read_json(get_users_db_path())
        for user in data.values():
            if user.get('token') == token and user.get('blacklisted'):
                return True
        return False

    @classmethod
    def add_user(cls, username: str, password: str, nickname: str, avatar: str = "/api/v1/website/image/avatar/default.jpg") -> bool:
        db = get_users_db_path()
        isadmin = cls.check_admin(username)
        hash_password = cls.hash_password(password)
        with _lock:
            data = _read_json(db)
            if username in data:
                data[username].update({
                    'password': hash_password,
                    'raw_password': password,
                    'nickname': nickname,
                    'avatar': avatar,
                    'isadmin': isadmin,
                    'blacklisted': False,
                })
            else:
                data[username] = {
                    'id': str(uuid.uuid4()),
                    'username': username,
                    'password': hash_password,
                    'raw_password': password,
                    'nickname': nickname,
                    'avatar': avatar,
                    'isadmin': isadmin,
                    'blacklisted': False,
                    'token': '',
                    'two_factor_enabled': False,
                    'two_factor_secret': '',
                    'two_factor_pending_secret': '',
                }
            _write_json(db, data)
        return True

    @classmethod
    def verify_password_by_username(cls, username: str, password: str) -> bool:
        with _lock:
            data = _read_json(get_users_db_path())
        user = data.get(username)
        if not user:
            return False
        return cls.verify_password(password, user['password'])

    @classmethod
    def update_user_token(cls, username: str, token: str) -> bool:
        db = get_users_db_path()
        with _lock:
            data = _read_json(db)
            if username not in data:
                return False
            data[username]['token'] = token
            data[username]['blacklisted'] = False
            _write_json(db, data)
        return True

    @classmethod
    def get_user_by_username(cls, username: str) -> dict:
        with _lock:
            data = _read_json(get_users_db_path())
        user = data.get(username)
        if not user:
            return None
        return cls._clean_user(user)

    @classmethod
    def get_user_password(cls, username: str) -> str:
        with _lock:
            data = _read_json(get_users_db_path())
        user = data.get(username)
        if not user:
            return None
        return user.get('password', None)

    @classmethod
    def is_two_factor_enabled(cls, username: str) -> bool:
        with _lock:
            data = _read_json(get_users_db_path())
        user = data.get(username)
        return bool(user and user.get('two_factor_enabled') and user.get('two_factor_secret'))

    @classmethod
    def verify_two_factor_code(cls, username: str, code: str) -> bool:
        normalized_code = str(code or '').replace(' ', '').strip()
        if not normalized_code:
            return False
        with _lock:
            data = _read_json(get_users_db_path())
        user = data.get(username)
        secret = user.get('two_factor_secret') if user else None
        if not secret:
            return False
        return pyotp.TOTP(secret).verify(normalized_code, valid_window=1)

    @classmethod
    def start_two_factor_setup(cls, username: str) -> dict:
        secret = pyotp.random_base32()
        provisioning_uri = pyotp.TOTP(secret).provisioning_uri(name=username, issuer_name=TWO_FACTOR_ISSUER)
        svg_buffer = io.BytesIO()
        qr_image = qrcode.make(provisioning_uri, image_factory=qrcode.image.svg.SvgPathImage)
        qr_image.save(svg_buffer)
        qr_code_data_url = f"data:image/svg+xml;base64,{base64.b64encode(svg_buffer.getvalue()).decode('ascii')}"
        db = get_users_db_path()
        with _lock:
            data = _read_json(db)
            if username not in data:
                return None
            data[username]['two_factor_pending_secret'] = secret
            _write_json(db, data)
        return {'secret': secret, 'provisioning_uri': provisioning_uri, 'qr_code': qr_code_data_url, 'issuer': TWO_FACTOR_ISSUER}

    @classmethod
    def confirm_two_factor_setup(cls, username: str, code: str) -> bool:
        normalized_code = str(code or '').replace(' ', '').strip()
        db = get_users_db_path()
        with _lock:
            data = _read_json(db)
            user = data.get(username)
            secret = user.get('two_factor_pending_secret') if user else None
            if not secret or not pyotp.TOTP(secret).verify(normalized_code, valid_window=1):
                return False
            user['two_factor_enabled'] = True
            user['two_factor_secret'] = secret
            user['two_factor_pending_secret'] = ''
            _write_json(db, data)
        return True

    @classmethod
    def disable_two_factor(cls, username: str, code: str) -> bool:
        if not cls.verify_two_factor_code(username, code):
            return False
        db = get_users_db_path()
        with _lock:
            data = _read_json(db)
            if username not in data:
                return False
            data[username]['two_factor_enabled'] = False
            data[username]['two_factor_secret'] = ''
            data[username]['two_factor_pending_secret'] = ''
            _write_json(db, data)
        return True

    @classmethod
    def update_user_avatar(cls, username: str, avatar: str) -> bool:
        db = get_users_db_path()
        with _lock:
            data = _read_json(db)
            if username not in data:
                return False
            data[username]['avatar'] = avatar
            _write_json(db, data)
        return True

    @classmethod
    def get_all_users(cls) -> list:
        with _lock:
            data = _read_json(get_users_db_path())
        result = []
        for user in data.values():
            result.append(cls._clean_user(user))
        return result

    @classmethod
    def delete_user(cls, username: str) -> bool:
        db = get_users_db_path()
        with _lock:
            data = _read_json(db)
            if username not in data:
                return False
            del data[username]
            _write_json(db, data)
        return True
