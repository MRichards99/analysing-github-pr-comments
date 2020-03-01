import logging
import json

import mysql.connector

logger = logging.getLogger('big-data-python')
SQL_CONFIG_PATH = '/home/xfu59478/big-data-work/analysing-github-pr-comments/db_config.json'

def open_db_connection():
    with open(SQL_CONFIG_PATH) as config_file:
        # Config contains: username, password, host and database
        sql_config = json.load(config_file)

    conn = mysql.connector.connect(**sql_config)

    return conn


def create_table(conn):
    TABLES = {}
    TABLES['pr_comments'] = (
        "CREATE TABLE `pr_comments` ("
        "  `COMMENT_ID` int NOT NULL,"
        "  `COMMIT_ID` varchar(50) NOT NULL,"
        "  `URL` varchar(150) NOT NULL,"
        "  `AUTHOR` varchar(100) NOT NULL,"
        "  `CREATED_AT` date NOT NULL,"
        "  `BODY` longtext NOT NULL)")

    cursor = conn.cursor()

    for name in TABLES:
        cursor.execute(TABLES[name])
        logger.info('Table created called: {}'.format(name))
