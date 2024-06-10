import psycopg2
import json


def connect():
    with open('config.json', 'r') as f:
        config = json.load(f)
        database_params = config['database']
        f.close()
    return psycopg2.connect(dbname=database_params['dbname'], user=database_params['user'],
                            password=database_params['password'], host=database_params['host'])
