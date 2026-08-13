from fastapi import UploadFile
from core.exceptions import InvalidFileTypeError


def validate_csv(file: UploadFile):
    if not file.filename.endswith(".csv"):
        raise InvalidFileTypeError()