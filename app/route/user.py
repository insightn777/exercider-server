from fastapi import Depends

from app.route import api_router, public_router
from domain.service import user as user_service


@api_router.post('/user', response_model=UserResponse, tags=['user'])
def create_user(user=Depends(user_service.create_user)):
    return user


@api_router.put('/user/me', response_model=UserResponse, tags=['user'])
def update_me(user=Depends(user_service.update_me)):
    return user


@api_router.delete('/user/me', tags=['user'])
def delete_user(result=Depends(user_service.delete_user)):
    return result


@public_router.post('/user/me/login', response_model=UserResponse, tags=['user'])
def login_user(response=Depends(user_service.login_user)):
    return response


@api_router.delete('/user/me/logout', tags=['user'])
def logout_user(response=Depends(user_service.logout_user)):
    return response


@api_router.post('/user/me/token', tags=['user'])
def refresh_access_token(response=Depends(user_service.refresh_access_token)):
    return response
