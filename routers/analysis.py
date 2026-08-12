from fastapi import APIRouter, File, UploadFile


router = APIRouter(prefix ="/api/v1/analysis", tags=["analysis"])


@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    return {"filename" : file.filename}