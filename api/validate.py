import json
from urllib.parse import unquote
import hmac
import hashlib

from fastapi import HTTPException, Request

import config
     

def convert_to_dict(init_data: str) -> dict:
     return {k: unquote(v) for k, v in [s.split('=', 1) for s in init_data.split('&')]}


def validate_init_data(init_data: dict, bot_token: str):
     # print(init_data['hash'])
     data_check_string = '\n'.join(f"{k}={v}" for k, v in sorted(init_data.items()) if k != 'hash')
     # print(init_data)

     secret_key = hmac.new("WebAppData".encode(), bot_token.encode(), hashlib.sha256).digest()
     h = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256)
     return h.hexdigest() == init_data['hash']

def validate(request: Request):
     data = convert_to_dict(request.headers['Authorization'])
     if validate_init_data(data, config.bot_token):
          data['user'] = json.loads(data['user'])
          return data
     raise HTTPException(
          status_code=400,
          detail='Authorization data incorrect!',
     )
          