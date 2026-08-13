import pandas as pd
import io

def read_csv_from_upload(file_bytes: bytes) -> pd.DataFrame:
    df = pd.read_csv(io.BytesIO(file_bytes))
    return df