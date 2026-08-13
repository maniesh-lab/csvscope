from fastapi import APIRouter, File, UploadFile
from services.analyzer import read_csv_from_upload, get_summary_stats


router = APIRouter(prefix ="/api/v1/analysis", tags=["analysis"])


@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    contents = await file.read()
    df = read_csv_from_upload(contents)
    stats = get_summary_stats(df)

    return {
        "filename" : file.filename,
        "rows":len(df),
        "stats": stats
    }
