from typing import List
from fastapi import APIRouter, Query, UploadFile, File
from fastapi.responses import HTMLResponse
from starlette.responses import JSONResponse
import json
from schemas import UserID, Dictionary, DictionaryDTO, WordDTO, DictionaryUpdate, WordUpdate
from utils import connect
from pdf_parser import parse_pdf

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
        cursor.execute('SELECT name, glosses, alphabet FROM "dictionary" WHERE user_id = %s AND id = %s',
                       (user_id, dict_id))
        row = cursor.fetchone()
    name, glosses, alphabet = row[0], row[1], row[2]
    with conn.cursor() as cursor:
        cursor.execute('SELECT id, text, glosses FROM "word" WHERE dict_id = %s', (dict_id,))
        rows = cursor.fetchall()
    return JSONResponse(status_code=200,
                        content={"name": name, "glosses": glosses, "words": rows, "alphabet": alphabet})


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


@router.post("/pdf")
async def pdf(file: UploadFile = File(...), user_id: int = Query()):
    file_location = f"{file.filename}"
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    parsed = parse_pdf(file_location)
    dict = parsed[0]
    alphabet = parsed[1]
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO "dictionary"(user_id, name, glosses, alphabet) VALUES (%s, %s, %s, %s)',
                       (user_id, file_location, json.dumps({"Definition": []}), alphabet))
    conn.commit()
    with conn.cursor() as cursor:
        cursor.execute('SELECT id FROM "dictionary" ORDER BY id DESC LIMIT 1')
        dict_id = cursor.fetchone()[0]
    for i in dict:
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO "word"(dict_id, text, glosses) VALUES (%s, %s, %s)',
                           (dict_id, i[0], json.dumps(i[1])))
    conn.commit()
    conn.close()
    return JSONResponse(status_code=201, content="Created")


@router.get("/", response_class=HTMLResponse)
async def main_page():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Upload PDF</title>
    </head>
    <body>
        <h1>Upload PDF File</h1>
        <form action="/dictionary/pdf?user_id=1" enctype="multipart/form-data" method="post">
            <input type="file" name="file" required>
            <button type="submit">Upload</button>
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
