import os

import psycopg2
import yaml


class KeyManager(object):
    def __init__(self):
        self.conn = self._create_connection()
        self._initialize_db_table()

    # Public
    def validate_api_key(self, key):
        query = f"SELECT count(key) FROM api_keys where key = '{key}';"
        cur = self.conn.cursor()

        cur.execute(query)
        output = cur.fetchone()[0]
        if output == 1:
            return True
        else:
            return False

    # Private
    def _create_connection(self):
        db_config = None
        path = os.path.abspath("NounExtraction/config.yaml")
        with open(path, "r") as file:
            db_config = yaml.safe_load(file)

        return psycopg2.connect(
            host=db_config["db"]["host"],
            database=db_config["db"]["dbname"],
            user=db_config["db"]["user"],
            password=db_config["db"]["password"],
        )

    def _initialize_db_table(self):
        query = (
            "CREATE TABLE IF NOT EXISTS api_keys ("
            "key char(32) NOT NULL,"
            "PRIMARY KEY (key))"
        )

        cursor = self.conn.cursor()

        cursor.execute(query)
        cursor.close()
        self.conn.commit()
