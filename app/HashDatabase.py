import sqlite3


class HashDatabase(object):
    def __init__(self, db_path="internal_db.db"):
        """
        Notes: If using sqlite, use this init function to check for a table, and
        initialize if it doesn't exist

        If using postgres, use this function to connect to the table and store
        that connection
        """
        self.con = sqlite3.connect(db_path)
        self.cache_table_name = "cache_db"
        self._setup_table()

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
        pass

    def add_new_results_to_hash(self, hash: str, nouns: str, update=False):
        """
        Given: A hash value and results in an array

        Steps if update == false:
        1. pass hash to check_for_existing_hash
        2. if hash exists, raise a ValueError
        3. if hash doesn't exist, insert nouns with an insert statement

        Steps if update == True:
        1. pass hash to check_for_existing_hash
        2. if hash exists, update the nouns for that hash with an update statement
        3. if hash does not exist, insert nouns for that hash with an insert statement
        """
        pass

    def get_nouns_from_hash(self, hash: str) -> str:
        """
        Given: a hash value
        Return: a string representation of a dictionary containing all of the identfied nouns

        Steps:
            - Accept a hash value
            - Search for a noun result in the databse
            - return the result
        """
        pass

    # private methods

    def _setup_table(self):
        cursor = self._return_new_cursor()

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS cache_db (
            hash CHARACTER(64) NOT NULL PRIMARY KEY,
            nouns TEXT)"""
        )

    def _return_new_cursor(self) -> sqlite3.Cursor:
        """
        Returns a new db cursor for executing queries

        Make sure to clean up after yourself. When you're done executing queries, run cursor.close()
        """
        return self.con.cursor()
