from fastapi import UploadFile

from core.exceptions import InvalidFileTypeError


def validate_csv(file: UploadFile):
    # .lower() so "DATA.CSV" is accepted too
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise InvalidFileTypeError()
