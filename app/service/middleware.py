from typing import Optional

import jwt
from fastapi import Cookie, Request, Depends

from configs import Config, get_settings


def check_token(request: Request, tk: Optional[str] = Cookie(None), setting: Config = Depends(get_settings)):
    if setting.TESTING:
        request.state.info = {
            'ulid': 'u04',
        }
    else:
        payload = jwt.decode(tk, setting.JWT_PUB_KEY, algorithms=["RS256"])
        request.state.info = payload
