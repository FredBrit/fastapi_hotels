from fastapi import APIRouter, HTTPException, Response, Request, Depends
from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService



router = APIRouter(prefix='/auth', tags=['Аутентификация и авторизация'])



@router.post('/login')
async def login_user(data: UserRequestAdd, response: Response, db: DBDep):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail='Пользователь с таким email не зарегистрирован')
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Неверный пароль')
    access_token = AuthService().create_access_token({'user_id': user.id})
    response.set_cookie('access_token', access_token)   
    return {'access_token': access_token}



@router.post('/register')
async def register_user(data: UserRequestAdd, db: DBDep):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)

    try:
        await db.users.add(new_user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    await db.commit()

    return {'status': 'OK'}   


@router.get('/me')
async def get_me(user_id: UserIdDep, db: DBDep):
    
    user = await db.users.get_one_or_none(id=user_id)

    return user


@router.post('/logout')
async def logout_me(response: Response, user_id: UserIdDep, db: DBDep):
    
    response.delete_cookie(key='access_token')
    return {'status': 'Разлогинился'}            
