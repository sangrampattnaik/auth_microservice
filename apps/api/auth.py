import jwt, datetime
from fastapi import APIRouter, Request, Depends, HTTPException
from apps.utils import get_db, Database, check_password
from apps.schemas.auth import UserIn, Login
from apps.models.auth import User, Session
from apps.core.config import settings
from fastapi.security import APIKeyHeader
import requests as req


router = APIRouter(prefix='/auth',tags=['auth'])
header_token = APIKeyHeader(
    name='Authorization'
)

def authenticate_token(token = Depends(header_token),db = Depends(get_db)):
    try:
        prefix, token = token.split()
        if prefix != "Bearer":
            # ...
            raise HTTPException(status_code=401,detail='unauthorized sss')
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
        if payload['token_type'] != 'access':
            print(payload)
            raise HTTPException(status_code=401,detail='unauthorized ssss')
            # ...
        db_ref = Database(db,User)
        # breakpoint()
        user = db_ref.get_by_any(id=payload['id'])
        if not user:
            raise HTTPException(status_code=401,detail='unauthorized ss')
        return user
    except KeyError:
        raise HTTPException(status_code=401,detail='unauthorized s')


@router.post('',status_code=201)
def create_user(body: UserIn, db = Depends(get_db)):
    db_ref = Database(db,User)
    if db_ref.get_by_any(username=body.username):
        raise HTTPException(status_code=404,detail='username already taken')
    data = body.dict()
    data.pop('confirm_password')
    user = db_ref.create(**data)
    return user


@router.post('/login',status_code=201)
def login(request: Request, body: Login, db = Depends(get_db)):
    db_ref = Database(db,User)
    user = db_ref.get_by_any(username=body.username)
    if not user:
        raise HTTPException(status_code=401,detail='authentication failed')
    if not check_password(user.password, body.password):
        raise HTTPException(status_code=401,detail='authentication failed')
    access_token_payload = {
        "id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION_IN_MINUTES),
        "token_type": "access"
    }
    refresh_token_payload = access_token_payload.copy()
    refresh_token_payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.REFRESH_TOKEN_EXPIRATION_IN_MINUTES)
    refresh_token_payload['token_type'] = 'refresh'
    access_token = jwt.encode(access_token_payload,settings.SECRET_KEY,'HS256')
    refresh_token = jwt.encode(refresh_token_payload,settings.SECRET_KEY,'HS256')
    ipinfo_response = req.get("https://ipinfo.io/json").json()
    db_session = Database(db,Session)
    db_session.create(
        access_token=access_token,    
        refresh_token=refresh_token,    
        city=ipinfo_response.get("city", None),
        country=ipinfo_response.get("country", None),
        region=ipinfo_response.get("region", None),
        ip=ipinfo_response.get("ip", None),
        user_agent=request.headers.get("User-Agent", None),
        timezone=ipinfo_response.get("timezone", None),
        loc=ipinfo_response.get("loc", None),
        user_id=user.id
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@router.get('/me',status_code=200)
def me(user = Depends(authenticate_token),db = Depends(get_db)):
    return user


@router.get('/refresh',status_code=200)
def me(user = Depends(authenticate_token),db = Depends(get_db)):


    return user