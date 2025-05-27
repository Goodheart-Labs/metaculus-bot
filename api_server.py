from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import os
from forecasting_tools import BinaryQuestion, GeneralLlm
from current_best_bot import get_best_bot

API_KEY = os.getenv("API_SERVER_KEY", "changeme")

app = FastAPI()

# Allow all origins for development; restrict in prod
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ForecastRequest(BaseModel):
    question: str
    resolution_criteria: str = ""
    fine_print: str | None = None
    background_info: str | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/forecast-binary")
async def forecast_binary(
    req: ForecastRequest,
    authorization: str = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Missing or invalid Authorization header")
    token = authorization.split(" ", 1)[1]
    if token != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    user_question = BinaryQuestion(
        question_text=req.question,
        resolution_criteria=req.resolution_criteria,
        fine_print=req.fine_print,
        background_info=req.background_info,
        id_of_post=-1,
        page_url="api://user-question"
    )
    bot = get_best_bot(publish_reports_to_metaculus=False)
    try:
        forecast_reports = await bot.forecast_questions([user_question], return_exceptions=True)
        # Just return the first report for now
        report = forecast_reports[0]
        # Return human-readable, valid JSON fields
        return {
            "reasoning": getattr(report, "summary", None),
            "prediction": getattr(report, "prediction", None)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
