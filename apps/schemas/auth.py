from pydantic import BaseModel, root_validator
from fastapi import HTTPException
from apps import utils


class UserIn(BaseModel):
    name: str
    username: str
    mobile: str
    password: str
    confirm_password: str
    
    
    @root_validator
    def validate_password(cls,values):
        password = values.get('password')
        confirm_password = values.get('confirm_password')

        if password != confirm_password:
            raise HTTPException(status_code=400,detail='password should match')
        values['password'] = utils.make_password(password)
        return values


class Login(BaseModel):
    username: str
    password: str
    