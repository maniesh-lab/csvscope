from typing import Optional

import pandas as pd
from fastapi import APIRouter, File, Query, UploadFile

from models.response import AnalysisResponse
from services.analyzer import get_summary_stats, read_csv_from_upload
from services.chart_builder import build_chart, encode_chart_to_base64, get_first_numeric_column
from utils.validators import validate_csv

router = APIRouter(prefix="/api/v1/analysis", tags=["analysis"])


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze(
    file: UploadFile = File(...),
    column: Optional[str] = Query(None, description="Column name to chart. Defaults to the first numeric column if not provided."),
):
    validate_csv(file)
    contents = await file.read()
    df = read_csv_from_upload(contents)
    stats = get_summary_stats(df)

    chart_column = column if column else get_first_numeric_column(df)

    chart_base64 = None
    message = None
    if chart_column is None:
        message = "No numeric columns found, so no chart was made."
    elif chart_column not in df.columns:
        message = f"Column '{chart_column}' not found. Available columns: {', '.join(map(str, df.columns))}."
    elif not pd.api.types.is_numeric_dtype(df[chart_column]):
        message = f"Column '{chart_column}' isn't numeric, so it can't be drawn as a histogram."
    else:
        fig = build_chart(df, chart_column)
        chart_base64 = encode_chart_to_base64(fig)

    return {
        "filename": file.filename,
        "rows": len(df),
        "stats": stats,
        "chart": chart_base64,
        "message": message,
    }
