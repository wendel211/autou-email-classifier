import os
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .services.extract import extract_text_from_upload
from .services.classifier import classify_email
from .services.responder import suggest_response

app = FastAPI(title="AutoU – Classificador de Emails")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/api/classify")
async def api_classify(file: UploadFile | None = File(default=None), text: str | None = Form(default=None)):
    body_text = (text or "").strip()
    if not body_text and file is not None:
        bytes_ = await file.read()
        body_text = await extract_text_from_upload(file.filename, bytes_)

    if not body_text:
        return JSONResponse({"error": "Texto vazio."}, status_code=400)

    result = classify_email(body_text)
    category = result.get("category", "Produtivo")
    confidence = result.get("confidence", 0.7)
    strategy = result.get("strategy", "rules")
   
    response_text = result.get("response") or suggest_response(body_text, category)
    return {
        "category": category,
        "confidence": confidence,
        "strategy": strategy,
        "response": response_text
    }
