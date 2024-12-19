from fastapi import FastAPI, Path, HTTPException, Body
from typing import Annotated, List
from pydantic import BaseModel, Field

app = FastAPI()
# users = {'1': 'Имя: Example, возраст: 18'}
users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/users", response_model=List[User])
async def get_users() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def create_user(username: Annotated[str, Path(min_length=5, max_length=20,
                                                    description='Enter username', example='Vasya_User')],
                      age: int = Path(ge=18, le=120, description='Enter age', example=36)) -> List[User]:
    user_id = len(users)
    if user_id < 1:
        user_id = 1
    else:
        user_id += 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return users


@app.put('/user/{user_id}/{username}/{age}')
async def update_users(user_id: int,
                       username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username')],
                       age: Annotated[int, Path(ge=18, le=120, description='Enter age')]):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_users(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail='User was not found')
#  python -m uvicorn module_16_4:app