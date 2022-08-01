import mysql.connector
from bot_create import dotenv


def create_connection():
    cnx = mysql.connector.connect(
        host=dotenv['DATABASE_HOST'],
        user=dotenv['DATABASE_USER'],
        password=dotenv['DATABASE_PASS'],
        database=dotenv['DATABASE']
    )
    cur = cnx.cursor()
    return cnx, cur
