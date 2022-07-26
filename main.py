# pylint: disable=E0611,E0401
from typing import List
from fastapi import FastAPI, HTTPException
from models import User_Pydantic, UserIn_Pydantic, Users
from pydantic import BaseModel

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

app = FastAPI()


class Status(BaseModel):
    message: str

@app.get('/')
async def get_status():
    return 'ayush here'


@app.get("/users")
async def get_users():
    return await User_Pydantic.from_queryset(Users.all())




@app.post("/users")
async def create_user(user: UserIn_Pydantic):
     user_obj = await Users.create(**user.dict(exclude_unset=True))
     return await User_Pydantic.from_tortoise_orm(user_obj)




@app.put("/user/{bank_id}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_user(bank_id: int, user: UserIn_Pydantic):
    await Users.filter(id=bank_id).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(Users.get(id=bank_id))




@app.delete("/user/{user_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_user(bank_id: int):
    deleted_count = await Users.filter(id=bank_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {bank_id} not found")
    return Status(message=f"Deleted user {bank_id}")


register_tortoise(
    app,
    db_url="postgresql://Databases:root@localhost:5432/postgres",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

