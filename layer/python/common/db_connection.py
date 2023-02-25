import os
import logging
import psycopg2


logger = logging.getLogger()
logger.setLevel(logging.INFO)


db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT", default=5432)
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_table = os.getenv("DB_TABLE")


def connect():
    try:
        conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (db_name, db_user, db_host, db_password))
        logger.info("Connected to database successfully")
        return conn
    except:
        logger.error("Unable to connect to database")


def close_connection(connection, cursor):
    if connection:
        cursor.close()
        connection.close()
        logger.info("Closed PostgreSQL connection successfully")
