import sqlite3


class HashDatabase(object):
    def __init__(self):
        """
        Notes: If using sqlite, use this init function to check for a table, and
        initialize if it doesn't exist

        If using postgres, use this function to connect to the table and store
        that connection
        """
        self.con = sqlite3.connect("internal_db.db")
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
        """

        return False

    def add_new_results_to_hash(self, hash: str, results: str):
        """
        Given: A hash value and results in an array

        Steps:
            - Perform a lookup to ensure a file for that hash exists
            - If file doesn't exists raise an exception
            - If file does exists and contains content raise and exception and
            log everything (previous content, new content, hash, datetime)
            - If hash exists and file is empty, store results in file
        """
        pass

    def get_nouns_from_hash(self, hash: str) -> dict:
        """
        Given: a hash value
        Return: a dictionary containing all of the identfied nouns

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
