class HashDatabase(object):
    def __init__(self):
        """
        Notes: If using sqlite, use this init function to check for a table, and
        initialize if it doesn't exist

        If using postgres, use this function to connect to the table and store
        that connection
        """
        pass

    # Public Methods
    def check_for_existing_hash(self, hash: int) -> tuple[bool, str]:
        """
        Given: A hash value
        Return: A bool representing whether this hash existed already

        Steps:
            - Perform a lookup to see if the has exists
            - If hash exists, return true and the path to that hashs results
            - If hash doesn't exists, create new record and file for results
            - Return false and None
        """

    def add_new_results_to_hash(self, hash: int, results: str):
        """
        Given: A hash value and results in an array

        Steps:
            - Perform a lookup to ensure a file for that hash exists
            - If file doesn't exists raise an exception
            - If file does exists and contains content raise and exception and
            log everything (previous content, new content, hash, datetime)
            - If hash exists and file is empty, store results in file
        """
