from fastapi import HTTPException


class InvalidFileTypeError(HTTPException):
    def __init__(self, detail: str = "Only CSV files are supported."):
        super().__init__(status_code=400, detail=detail)


class InvalidCSVError(HTTPException):
    def __init__(self, detail: str = "The file couldn't be read as a CSV. Check that it's a valid, comma-separated file."):
        super().__init__(status_code=400, detail=detail)


class EmptyCSVError(HTTPException):
    def __init__(self, detail: str = "The uploaded CSV file is empty."):
        super().__init__(status_code=400, detail=detail)