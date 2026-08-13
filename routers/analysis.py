from fastapi import APIRouter, File, UploadFile, Query
from services.analyzer import read_csv_from_upload, get_summary_stats
from services.chart_builder import get_first_numeric_column, build_chart, encode_chart_to_base64
from models.response import AnalysisResponse
from utils.validators import validate_csv

router = APIRouter(prefix="/api/v1/analysis", tags=["analysis"])


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze(
    file: UploadFile = File(...),
    column: str = Query(None, description="Column name to chart. Defaults to the first numeric column if not provided.")):
    
    validate_csv(file)
    contents = await file.read()
    df = read_csv_from_upload(contents)
    stats = get_summary_stats(df)

    chart_column = column if column else get_first_numeric_column(df)

    chart_base64 = None
    if chart_column and chart_column in df.columns:
        fig = build_chart(df, chart_column)
        chart_base64 = encode_chart_to_base64(fig)

    return {
        "filename": file.filename,
        "rows": len(df),
        "stats": stats,
        "chart": chart_base64
    }