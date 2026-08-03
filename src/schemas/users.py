from pydantic import BaseModel, ConfigDict, EmailStr

class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str
    
    model_config = ConfigDict(from_attributes=True)

class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)

class User(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class UserWithHashedPassword(User):
    hashed_password: str
    
    model_config = ConfigDict(from_attributes=True)    