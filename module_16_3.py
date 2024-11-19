from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()
users_db = {'1': 'Имя: Example, Возраст: 18'}


@app.get("/users")
async def get_all_users() -> dict:
    return users_db


@app.post("/user/{username}/{age}")
async def reg_new_users(username: Annotated[
    str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanStudent')],
                        age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=25)]) -> str:
    user_id = str(int(max(users_db, key=int)) + 1)
    message = f'Имя: {username}, Возраст: {age}'
    users_db[user_id] = message
    ans = f'User {user_id} is registered.'
    return ans


@app.put("/user/{user_id}/{username}/{age}")
async def update_users_db(username: Annotated[
    str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanStudent')],
                          age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=25)],
                          user_id: int = Path(ge=0)) -> str:
    message = f'Имя: {username}, Возраст: {age}'
    users_db[user_id] = message
    ans = f'User {user_id} is updated.'
    return ans


@app.delete("/user/{user_id}")
async def delete_user(user_id: str) -> str:
    del users_db[user_id]
    ans = f"User {user_id} is deleted"
    return ans
