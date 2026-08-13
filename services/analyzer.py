import pandas as pd
import io

def read_csv_from_upload(file_bytes: bytes) -> pd.DataFrame:
    df = pd.read_csv(io.BytesIO(file_bytes))
    return df

def get_summary_stats(df: pd.DataFrame) -> dict:
    stats_df = df.describe()   #calculate mean, std, min, max, etc. per numeric column

    # .astype(object)   -> removes strict float type so None is allowed to stick
    # .where(...)       -> replaces any NaN values with None
    # .to_dict()        -> converts to plain dict so it can be sent back as JSON
    return stats_df.astype(object).where(pd.notnull(stats_df), None).to_dict()