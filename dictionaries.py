from typing import List
from fastapi import APIRouter, Query
from starlette.responses import JSONResponse
import json
import psycopg2
from schemas import UserID, Dictionary, DictionaryDTO

router = APIRouter(prefix="/dictionary", tags=["dictionaries"])


@router.get("/list")
async def dictionary_list(user_id: int = Query()) -> List[Dictionary]:
    with open('config.json', 'r') as f:
        config = json.load(f)
        database_params = config['database']
        f.close()
    conn = psycopg2.connect(dbname=database_params['dbname'], user=database_params['user'],
                            password=database_params['password'], host=database_params['host'])
    with conn.cursor() as cursor:
        cursor.execute('SELECT id, name FROM "dictionary" WHERE user_id = %s', (user_id,))
        rows = cursor.fetchall()
    conn.close()
    return JSONResponse(status_code=200, content=rows)


@router.post("/create")
async def dictionary_create(dictionary: DictionaryDTO):
    with open('config.json', 'r') as f:
        config = json.load(f)
        database_params = config['database']
        f.close()
    conn = psycopg2.connect(dbname=database_params['dbname'], user=database_params['user'],
                            password=database_params['password'], host=database_params['host'])
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO "dictionary"(user_id, name, glosses) VALUES (%s, %s, %s)',
                       (dictionary.user_id, dictionary.name, json.dumps(dictionary.glosses)))
    conn.commit()
    conn.close()
    return JSONResponse(status_code=201, content="Created")


@router.get("/words")
async def dictionary_words(user_id: int = Query(), dict_id: int = Query()):
    with open('config.json', 'r') as f:
        config = json.load(f)
        database_params = config['database']
        f.close()
    conn = psycopg2.connect(dbname=database_params['dbname'], user=database_params['user'],
                            password=database_params['password'], host=database_params['host'])
    with conn.cursor() as cursor:
        cursor.execute('SELECT name, glosses FROM "dictionary" WHERE user_id = %s AND id = %s', (user_id, dict_id))
        row = cursor.fetchone()
    name, glosses = row[0], row[1]
    with conn.cursor() as cursor:
        cursor.execute('SELECT text, glosses FROM "word" WHERE dict_id = %s', (dict_id,))
        rows = cursor.fetchall()
