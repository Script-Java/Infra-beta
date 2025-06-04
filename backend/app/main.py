from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from analyzer import DataAnalyzer
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional
import json
from renderer import Renderer
from duckdb_services import get_duckdb_schema, run_duckdb_query

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
app = FastAPI()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    query: str
    history: Optional[List[ChatMessage]] = None

@app.post('/summary')
async def analyze(file: UploadFile = File(...)):
    data_analyzer = DataAnalyzer(key=OPENAI_KEY, data=file.file)
    summary = data_analyzer.ai_summary()
    return {
        "ai_summary": summary
    }

@app.post('/json')
async def json_analysis(file: UploadFile = File(...)):
    analyzer = DataAnalyzer(key=OPENAI_KEY, data=file.file)
    json_result = analyzer.ai_json()
    return {
        "json": json_result
    }

@app.post("/chat")
async def chat(
    file: UploadFile = File(...),
    query: str = Form(...),
    history: Optional[str] = Form(None)  # Expecting JSON string
):
    analyzer = DataAnalyzer(key=OPENAI_KEY, data=file.file)

    # Convert history string to list of (role, content) tuples
    chat_history = None
    if history:
        try:
            parsed = json.loads(history)
            chat_history = [(msg["role"], msg["content"]) for msg in parsed]
        except Exception as e:
            return {"error": "Invalid history format", "details": str(e)}

    response = analyzer.data_chat(user_query=query, chat_history=chat_history)
    return {"response": response}

@app.post("/chat_stream")
async def chat_stream(
    file: UploadFile = File(...),
    query: str = Form(...),
    history: Optional[str] = Form(None)
):
    analyzer = DataAnalyzer(key=OPENAI_KEY, data=file.file)

    chat_history = None
    if history:
        try:
            parsed = json.loads(history)
            chat_history = [(msg["role"], msg["content"]) for msg in parsed]
        except Exception:
            return {"error": "Invalid history format"}

    def event_stream():
        for delta in analyzer.data_chat_stream(user_query=query, chat_history=chat_history):
            yield delta

    return StreamingResponse(event_stream(), media_type="text/plain")

@app.post('/report')
async def report(file: UploadFile = File(...)):
    analyzer = DataAnalyzer(key=OPENAI_KEY, data=file.file)
    report = analyzer.data_report_builder()
    return {
        "report": report
    }

@app.post("/charts")
async def generate_charts(file: UploadFile = File(...)):
    analyzer = DataAnalyzer(key=OPENAI_KEY, data=file.file)
    chart_instructions = analyzer.ai_json()  # This should return your chart JSON list

    renderer = Renderer(charts=chart_instructions, df=analyzer.df)
    rendered = renderer.render_charts()

    return {"charts": rendered}

@app.post("/sql")
async def run_sql(file: UploadFile = File(...), query: str = Form(...)):
    return run_duckdb_query(file, query)

@app.post("/sql_schema")
async def sql_schema(file: UploadFile = File(...)):
    return get_duckdb_schema(file)
