from fastapi import APIRouter, Depends, Request
from starlette.responses import JSONResponse
from random import randint
from schemas import User, UserLogin
import json
import psycopg2

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
async def register(user: User):
    with open('config.json', 'r') as f:
        config = json.load(f)
        database_params = config['database']
        f.close()
    conn = psycopg2.connect(dbname=database_params['dbname'], user=database_params['user'],
                            password=database_params['password'], host=database_params['host'])
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM "user" WHERE login = %s', (user.login,))
        if len(cursor.fetchall()) != 0:
            return JSONResponse(status_code=409, content="Login already used")
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO "user" (login, hash_password) '
                       'VALUES (%s, %s)', (user.login, user.hash_password))
    conn.commit()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id FROM "user" WHERE login = %s', (user.login,))
        user_id = cursor.fetchone()[0]
    conn.close()
    return JSONResponse(status_code=201, content=f"{user_id}")


@router.post("/login")
async def login(user: User):
    with open('config.json', 'r') as f:
        config = json.load(f)
        database_params = config['database']
        f.close()
    conn = psycopg2.connect(dbname=database_params['dbname'], user=database_params['user'],
                            password=database_params['password'], host=database_params['host'])
    with conn.cursor() as cursor:
        cursor.execute('SELECT id FROM "user" WHERE login = %s AND hash_password = %s',
                       (user.login, user.hash_password))
        user_id = cursor.fetchone()
        if user_id is None:
            return JSONResponse(status_code=404, content="Not found")
    conn.close()
    return JSONResponse(status_code=200, content=f"{user_id[0]}")
