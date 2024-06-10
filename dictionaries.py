from typing import List
from fastapi import APIRouter, Query
from starlette.responses import JSONResponse
import json
from schemas import UserID, Dictionary, DictionaryDTO, WordDTO, DictionaryUpdate, WordUpdate
from utils import connect

router = APIRouter(prefix="/dictionary", tags=["dictionaries"])


@router.get("/list")
async def dictionary_list(user_id: int = Query()) -> List[Dictionary]:
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id, name FROM "dictionary" WHERE user_id = %s', (user_id,))
        rows = cursor.fetchall()
    conn.close()
    return JSONResponse(status_code=200, content=rows)


@router.post("/create")
async def dictionary_create(dictionary: DictionaryDTO):
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO "dictionary"(user_id, name, glosses) VALUES (%s, %s, %s)',
                       (dictionary.user_id, dictionary.name, json.dumps(dictionary.glosses)))
    conn.commit()
    conn.close()
    return JSONResponse(status_code=201, content="Created")


@router.get("/words")
async def dictionary_words(user_id: int = Query(), dict_id: int = Query()):
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute('SELECT name, glosses FROM "dictionary" WHERE user_id = %s AND id = %s', (user_id, dict_id))
        row = cursor.fetchone()
    name, glosses = row[0], row[1]
    with conn.cursor() as cursor:
        cursor.execute('SELECT id, text, glosses FROM "word" WHERE dict_id = %s', (dict_id,))
        rows = cursor.fetchall()
    return JSONResponse(status_code=200, content={"name": name, "glosses": glosses, "words": rows})


@router.post("/word")
async def dictionary_word(word: WordDTO, dict_id: int = Query()):
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO "word"(dict_id, text, glosses) VALUES (%s, %s, %s)',
                       (dict_id, word.text, json.dumps(word.glosses)))
    conn.commit()
    conn.close()
    return JSONResponse(status_code=201, content="Created")


@router.put("/update")
async def dictionary_update(dict: DictionaryUpdate):
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute('UPDATE "dictionary" SET name = %s, glosses = %s WHERE id = %s',
                       (dict.name, json.dumps(dict.glosses), dict.dict_id))
    conn.commit()
    conn.close()
    return JSONResponse(status_code=200, content="Updated")


@router.delete("/delete")
async def dictionary_delete(dict_id: int = Query()):
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM "dictionary" WHERE id = %s', (dict_id,))
    conn.commit()
    conn.close()
    return JSONResponse(status_code=200, content="Deleted")


@router.put("/word")
async def update_word(word: WordUpdate):
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute('UPDATE "word" SET text = %s, glosses = %s WHERE id = %s',
                       (word.text, json.dumps(word.glosses), word.id))
    conn.commit()
    conn.close()
    return JSONResponse(status_code=200, content="Updated")


@router.delete("/word")
async def delete_word(id: int = Query()):
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM "word" WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    return JSONResponse(status_code=200, content="Deleted")
