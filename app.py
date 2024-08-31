from datetime import datetime
import os
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.main import api_dp
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler

from api.diary.report import SAVE_PATH


def check_reports():
    current_date = datetime.now()
    for file in os.listdir(SAVE_PATH):
        m_time = os.path.getmtime(SAVE_PATH + file)
        dt_m = datetime.fromtimestamp(m_time)
        diff = current_date - dt_m
        days, seconds = diff.days, diff.seconds
        hours = days * 24 + seconds // 3600
        if (hours >= 1): 
            os.remove(SAVE_PATH + file)


@asynccontextmanager
async def lifespan(app:FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_reports,"interval", hours=1)
    scheduler.start()
    yield

app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_dp)

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True, port=5000)