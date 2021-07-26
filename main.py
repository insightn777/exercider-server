from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.route import api_router, public_router
from app.service.errorhandler import init_error_handler
from configs import Config, get_settings


def create(config: Config) -> FastAPI:
    _app = FastAPI(**config.app_config)
    init_error_handler(_app)

    # app.add_middleware(CheckTokenMiddleware)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_DOMAIN,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.include_router(api_router)
    _app.include_router(public_router)

    return _app


app = create(get_settings())
