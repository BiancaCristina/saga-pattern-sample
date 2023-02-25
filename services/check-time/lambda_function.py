# Route: Check Time


import json
import psycopg2
import logging
from datetime import datetime
from common import db_connection


logger = logging.getLogger()
logger.setLevel(logging.INFO)


class TimeLimitException(Exception):
    """
    Simple class to indicate an error when attempt to
    updated a route that exceed the time limit
    """
    pass


def check_time_limit(trip):
    # Trip is a tuple formed by (id, created_at)
    current_time = datetime.now()
    trip_created_at = trip[1]
    difference_in_minutes = (abs(current_time - trip_created_at)).total_seconds() / 60
    if difference_in_minutes > 5:
        raise TimeLimitException("Unable to update route due to time limit exceeded")
    else:
        logger.info("Trip is allowed to be updated")


def find_trip(external_id: str):
    try:
        connection = db_connection.connect()
        cursor = connection.cursor()
        trip_query = """
        SELECT external_id, created_at FROM trip WHERE external_id = %s
        """
        cursor.execute(trip_query, (external_id,))
        trip = cursor.fetchone()
        return trip
    except(Exception, psycopg2.Error) as error:
        logger.error("Error when attempt to find trip", error)
    finally:
        db_connection.close_connection(connection, cursor)


def lambda_handler(event, context):
    logger.info("Received event: {}".format(event))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info("Converted message: {}".format(message))
    external_id = message['trip']['externalId']
    trip = find_trip(external_id)
    check_time_limit(trip)
    return {
        'statusCode': 204
    }