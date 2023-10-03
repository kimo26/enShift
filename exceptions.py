class DatabaseError(Exception):
    """
    Base class for database-related errors.
    """
    def __init__(self, message="A database error occurred."):
        self.message = message
        super().__init__(self.message)


class RecordNotFoundError(DatabaseError):
    """
    Raised when a record is not found in the database.
    """
    def __init__(self, message="The requested record was not found in the database."):
        self.message = message
        super().__init__(self.message)


class APIError(Exception):
    """
    Base class for API-related errors.
    """
    def __init__(self, message="An API error occurred."):
        self.message = message
        super().__init__(self.message)


class APINotFoundError(APIError):
    """
    Raised when an API endpoint returns a not found response.
    """
    def __init__(self, message="The requested resource was not found in the API."):
        self.message = message
        super().__init__(self.message)


class DataNotFoundError(Exception):
    """
    Raised when expected data isn't found in the database or API response.
    """
    def __init__(self, message="The expected data was not found."):
        self.message = message
        super().__init__(self.message)
