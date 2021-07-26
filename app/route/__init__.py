import importlib

from fastapi import APIRouter, Depends

from app.service.middleware import check_token

public_router = APIRouter(
    prefix="/public",
    tags=["public"],
)

api_router = APIRouter(
    prefix="/",
    dependencies=[Depends(check_token)],
)

importlib.import_module('app.route.user')
