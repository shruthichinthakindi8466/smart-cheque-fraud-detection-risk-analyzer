import base64
import json
import os
import sqlite3
import tempfile
from datetime import datetime
from typing import Any, Dict, List, Tuple

import cv2
import numpy as np
import pytesseract
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image, ImageOps, ImageEnhance

from app.analysis import analyze_cheque_image
from app.database import init_db, save_result

app = FastAPI(title="Smart Cheque Fraud Detection & Risk Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.post("/analyze")
async def analyze(
    cheque_image: UploadFile = File(..., description="Cheque image"),
    reference_signature: UploadFile = File(..., description="Reference signature"),
):
    try:
        cheque_ext = os.path.splitext(cheque_image.filename)[1].lower()
        sig_ext = os.path.splitext(reference_signature.filename)[1].lower()

        if cheque_ext not in {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp"}:
            return JSONResponse(status_code=400, content={"detail": "Invalid cheque file type."})
        if sig_ext not in {".jpg", ".jpeg", ".png"}:
            return JSONResponse(status_code=400, content={"detail": "Invalid reference signature file type."})

        with tempfile.NamedTemporaryFile(delete=False, suffix=cheque_ext) as cheque_tmp:
            cheque_tmp.write(await cheque_image.read())
            cheque_path = cheque_tmp.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=sig_ext) as sig_tmp:
            sig_tmp.write(await reference_signature.read())
            sig_path = sig_tmp.name

        result = analyze_cheque_image(cheque_path, sig_path)
        save_result(result)

        os.unlink(cheque_path)
        os.unlink(sig_path)

        return JSONResponse(content=result)
    except Exception as exc:  # pragma: no cover
        return JSONResponse(status_code=500, content={"detail": str(exc)})


@app.get("/health")
def health_check():
    return {"status": "ok"}
