import psycopg2
from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from dotenv import load_dotenv, dotenv_values
from starlette import status


def get_connection():
    try:
        db_config = dotenv_values(".env_shared")
        db_config_pass = dotenv_values(".env_sec")

        db_host = db_config['DB_HOST']
        db_username = db_config['DB_USERNAME']
        db_password = db_config_pass['DB_PASSWORD']
        db_name = db_config['DB_NAME']
        print("trying to connect to database")
        connection = psycopg2.connect(database=db_name, user=db_username, password=db_password,
                                      host=db_host, port="5432", cursor_factory=RealDictCursor)
        return connection
    except Exception as e:
        return None


def close_connection(conn):
    try:
        conn.close()
    except Exception as e:
        print(e)
        return None
