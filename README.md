# Smart Cheque Fraud Detection & Risk Analyzer

A full-stack web application for analysing cheque images, comparing them against a reference signature, extracting OCR fields, and producing a transparent risk assessment dashboard.

## Stack

- Frontend: React + Vite
- Backend: FastAPI + Python
- Processing: OpenCV, NumPy, Pillow, scikit-image, Tesseract OCR
- Database: SQLite

## Features

- Real file upload for cheque and reference signature
- Drag-and-drop upload UX
- OCR extraction for cheque details
- Signature similarity comparison
- Alteration/forgery analysis with annotated regions
- Risk scoring and fraud-risk dashboard
- SQLite persistence for analysis logs

## Local setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Then open the frontend Vite dev server in the browser.

## API

- POST /analyze
  - form-data fields: cheque_image, reference_signature

## Notes

- Bounce status is reported as `NOT CONFIRMED` and is explicitly separated from image-based risk analysis.
- The application does not claim definite forgery; it reports `No obvious alteration`, `Possible alteration`, or `High-risk alteration` based on image evidence.
