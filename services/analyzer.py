import pandas as pd
import io

def read_csv_from_upload(file_bytes: bytes) -> pd.DataFrame:
    df = pd.read_csv(io.BytesIO(file_bytes))
    return df

def get_summary_stats(df: pd.DataFrame) -> dict:
    stats_df = df.describe()
    return stats_df.astype(object).where(pd.notnull(stats_df), None).to_dict()