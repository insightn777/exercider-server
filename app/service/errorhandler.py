import traceback
from typing import Optional

from fastapi import status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.exc import NoResultFound
from starlette.exceptions import HTTPException as StarletteHTTPException


class BadRequestError(StarletteHTTPException):
    def __init__(self, msg: str, code: str = '400'):
        super().__init__(status_code=400, detail=msg)
        self.code = code


class ApplicationError(StarletteHTTPException):
    def __init__(self, msg: Optional[str], code: str = '0000'):
        super().__init__(status_code=500, detail=msg)
        self.code = code


class AuthorizationError(StarletteHTTPException):
    def __init__(self, msg: str, code: str = '401'):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=msg)
        self.code = code


def error_info(request, error):
    info = traceback.format_exc()
    try:
        return f"{request.method}:{request.path} | {str(request.values.to_dict())} | {error}\n{info}"
    except Exception:
        return f"{request.method}:{request.path} | {str(request.values.to_dict())} | {str(error).encode('utf-8')}\n{info}"


def init_error_handler(app):
    @app.exception_handler(ExpiredSignatureError)
    def expired_token_exception_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "result": 'N',
                "message": "Expired Token Error",
                "code": '4011',
            })

    @app.exception_handler(InvalidTokenError)
    def invalid_token_exception_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "result": 'N',
                "message": "Invalid Token Error",
                "code": '4010',
            })

    @app.exception_handler(RequestValidationError)
    @app.exception_handler(StarletteHTTPException)
    def http_exception_handler(request: Request, exc):
        try:
            status_code = exc.status_code
        except AttributeError:
            status_code = 400

        print(exc)

        try:
            message = str(exc.detail)
        except AttributeError:
            message = str(exc)

        try:
            code = exc.code
        except AttributeError:
            code = '0000'

        return JSONResponse(
            status_code=status_code,
            content={
                "message": message,
                "code": code,
            })

    @app.exception_handler(NoResultFound)
    def http_exception_handler(request: Request, exc):
        return JSONResponse(
            status_code=404,
            content={
                "message": "NoResultFound",
                "code": 4040,
            })
