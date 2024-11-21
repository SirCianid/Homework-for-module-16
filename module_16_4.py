from fastapi import FastAPI, Path, Body, HTTPException
from typing import Annotated, List, Optional
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI()


class User(BaseModel):
    id: Optional[int] = None
    username: str = Field(min_length=5, max_length=20, description='Enter username', example='UrbanStudent')
    age: int = Field(ge=18, le=120, description='Enter age', example=25)


users: List[User] = []


@app.get("/users", response_model=List[User])
async def get_all_users():
    return users


@app.post("/user", response_model=User)
async def reg_new_users(user: User):
    if users:
        user.id = max(users, key=lambda usr: usr.id or 0).id + 1
    else:
        user.id = 1
    new_user = User(id=user.id, username=user.username, age=user.age)
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}", response_model=User)
async def update_users_db(user_id: int, user: User):
    for i, u in enumerate(users):
        if u.id == user_id:
            users[i] = User(id=user_id, username=user.username, age=user.age)
            return users[i]
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}", response_model=User)
async def delete_user(user_id: int):
    for i, u in enumerate(users):
        if u.id == user_id:
            deleted_user = users.pop(i)
            return deleted_user
    raise HTTPException(status_code=404, detail="User was not found")


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')

