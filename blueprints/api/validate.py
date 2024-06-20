import hmac
import hashlib
from urllib.parse import unquote


def data_to_dict(init_data: str) -> dict:
     print(init_data)
     return {k: unquote(v) for k, v in [s.split('=', 1) for s in init_data.split('&')]}
     

def validate_init_data(init_data: dict, bot_token: str):
     data_check_string = '\n'.join(f"{k}={v}" for k, v in sorted(init_data.items()) if k != 'hash')

     secret_key = hmac.new("WebAppData".encode(), bot_token.encode(), hashlib.sha256).digest()
     h = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256)
     return h.hexdigest() == init_data['hash']
