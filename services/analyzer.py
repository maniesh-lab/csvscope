import io

import pandas as pd

from core.exceptions import EmptyCSVError, InvalidCSVError


def read_csv_from_upload(file_bytes: bytes) -> pd.DataFrame:
    if not file_bytes.strip():
        raise EmptyCSVError  # a 0-byte (or whitespace-only) file

    # Try UTF-8 first (utf-8-sig also strips the invisible "BOM" mark Excel
    # adds). If that fails, fall back to latin-1, the other common encoding
    # for CSVs exported from older spreadsheet programs.
    for encoding in ("utf-8-sig", "latin-1"):
        try:
            df = pd.read_csv(io.BytesIO(file_bytes), encoding=encoding)
            break
        except UnicodeDecodeError:
            continue
        except pd.errors.EmptyDataError:
            raise EmptyCSVError
        except pd.errors.ParserError:
            raise InvalidCSVError

    if df.empty:
        raise EmptyCSVError  # headers only, no data rows
    return df


def get_summary_stats(df: pd.DataFrame) -> dict:
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.empty:
        return {}  # no number columns, so there are no stats to give

    stats_df = numeric_df.describe()  # mean, std, min, max, etc. per number column

    # .astype(object)   -> removes strict float type so None is allowed to stick
    # .where(...)       -> replaces any NaN values with None
    # .to_dict()        -> converts to plain dict so it can be sent back as JSON
    return stats_df.astype(object).where(pd.notnull(stats_df), None).to_dict()
