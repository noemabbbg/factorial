from datetime import timedelta
import datetime

import jwt
from django.conf import settings


def create_token(user_id: int):
    access_token_expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
    return {
        'user_id': user_id,
        'access_token': create_access_token(
            data={'user_id': user_id}, expires_delta=access_token_expires
        ),
        'token_type': 'Token'
    }


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + timedelta(minutes=5)
    to_encode.update({'exp': expire, 'sub': 'access'})
    encode_jwt = jwt.encode(to_encode, settings.SIMPLE_JWT['SIGNING_KEY'], algorithm=settings.SIMPLE_JWT['ALGORITHM'])
    return encode_jwt
