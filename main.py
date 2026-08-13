from fastapi import FastAPI
from routers.analysis import router as analysis_router

app = FastAPI(title="csvscope")

app.include_router(analysis_router)

