from fastapi import APIRouter, File, UploadFile
from services.analyzer import read_csv_from_upload, get_summary_stats
from services.chart_builder import get_first_numeric_column,build_chart, encode_chart_to_base64

router = APIRouter(prefix ="/api/v1/analysis", tags=["analysis"])


@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    contents = await file.read()
    df = read_csv_from_upload(contents)
    stats = get_summary_stats(df)

    column = get_first_numeric_column(df)
    chart_base64 = None
    if column:
        fig = build_chart(df, column)
        chart_base64 = encode_chart_to_base64(fig)

    return {
        "filename" : file.filename,
        "rows": len(df),
        "stats": stats,
        "chart": chart_base64
    }

    
