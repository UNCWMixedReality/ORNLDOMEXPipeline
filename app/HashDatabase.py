import copy
import json
import sqlite3

from app.ClassifiedText import ClassifiedText, ClassifiedTextEncoder

# TODO: Add option to sync to PostgresDB instead of sqlite


class HashDatabase(object):
    """
    A database abstraction layer which utilizes either sqlite or postgres in order
    to track queried texts in order to cut down on API requests. All new text
    classification requests first pass through this object to see if the object
    has been analyzed already. If so, the API call is aborted and the previous results
    are returned. If not, the results of the call are stored here for later use
    """

    def __init__(self, postgres=False, db_path="internal_db.db"):
        """
        Note, postgres utilization should be specified at runtime, if that backend is
        desired. Otherwise this system will default to sqlite implementation of the database
        """
        if postgres is False:
            self.postgres = False
            self.con = sqlite3.connect(db_path)
            self.cache_table_name = "text_classification_results"
            self._setup_table()
        else:
            self.postgres = True
            raise NotImplementedError(
                "Postgres support has not yet been implemented. Please use Sqlite"
            )

    # Public Methods
    def check_for_existing_hash(self, hash: str) -> bool:
        """
        Given: A hash value
        Return: A bool representing whether this hash existed already

        Steps:
            - Perform a lookup to see if the hash exists
            - If hash exists, return true
            - If hash doesn't exist, return false
            - Throw a ValueError if the hash isn't a string
            - Throw a ValueError if the length of the hash is not 64
        """
        if not isinstance(hash, str):
            raise ValueError("Hashes must be of the string type")

        if len(hash) != 64:
            raise ValueError("Hashes must be 64 digits total")

        query = f'SELECT COUNT(hash) FROM {self.cache_table_name} WHERE hash = "{hash}"'

        output = self._select_count(query)

        if output == 1:
            return True
        else:
            return False

    def add_new_results_to_database(
        self, obj_to_store: ClassifiedText, update: bool = False
    ):
        """
        Given: A ClassifiedText object and optionally an update boolean
        Execute: A query which stores the ClassifiedObject based off user input

        Note: Before dumping to JSON we strip the hash from the ClassifiedText object.
        This is done because we already store the hash in the 'hash' column. This could
        be refactored to create a child object in ClassifiedText which just holds points
        and categories, but for now we'll do it this way

        TODO: Refactor ClassifiedText to include a smaller object which only holds the points
        and categories. Store this instead, eliminating the hash-stripping logic
        """

        # if we want to update the record and a hash exists
        if update and self.check_for_existing_hash(obj_to_store.parent_hash):

            # Grab the current record
            current_classified_text = self.get_classified_text_from_hash(
                obj_to_store.parent_hash
            )

            # Merge current and new. Strip hash
            merged_classified_text = current_classified_text + obj_to_store
            merged_classified_text.parent_hash = None

            # dump to json form
            data_to_store = json.dumps(
                merged_classified_text, cls=ClassifiedTextEncoder
            )

            # save to database
            query = f"UPDATE {self.cache_table_name} SET text_classification_results = {data_to_store} WHERE hash = {obj_to_store.parent_hash}"
            self._execute_query_and_return_results(query)

        # If we don't want to update and a hash may or may not exist
        else:

            # save and then strip hash
            hash = copy.deepcopy(obj_to_store.parent_hash)
            obj_to_store.parent_hash = None

            # dump to json form
            data_to_store = json.dumps(obj_to_store, cls=ClassifiedTextEncoder)

            # Generate Query
            if self.check_for_existing_hash(hash=hash):
                query = f"UPDATE {self.cache_table_name} SET text_classification_results = {data_to_store} WHERE hash = {obj_to_store.parent_hash};"
            else:
                query = f"INSERT INTO {self.cache_table_name} VALUES (\"{hash}\", '{data_to_store}');"

            # Execute Query
            self._execute_query_and_return_results(query)

    def get_classified_text_from_hash(self, hash: str) -> ClassifiedText:
        """
        Given: a hash value
        Return: a string representation of a dictionary containing all of the identfied nouns

        Steps:
            - Accept a hash value
            - Search for a noun result in the databse
            - return the result
        """

        query = f'SELECT * FROM {self.cache_table_name} WHERE hash = "{hash}"'
        results = self._execute_query_and_return_results(query)
        print(results[0][1])
        json_form = json.loads(results[0][1])
        return ClassifiedText(parent_hash=hash, json_str=json_form)

    # private methods

    def _select_count(self, query: str) -> int:
        result = self._execute_query_and_return_results(query)

        return result[0][0]

    def _execute_query_and_return_results(self, query: str) -> list:

        if self.postgres:
            raise NotImplementedError(
                "Postgres support has not yet been implemented. Please use Sqlite"
            )
        else:

            cursor = self._return_new_cursor()
            cursor.execute(query)
            output = cursor.fetchall()
            cursor.close()
            return output

    def _setup_table(self):
        cursor = self._return_new_cursor()

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS text_classification_results (
            hash CHARACTER(64) NOT NULL PRIMARY KEY,
            classified_text TEXT)"""
        )

    def _return_new_cursor(self) -> sqlite3.Cursor:
        """
        Returns a new db cursor for executing queries

        Make sure to clean up after yourself. When you're done executing queries, run cursor.close()
        """
        return self.con.cursor()
