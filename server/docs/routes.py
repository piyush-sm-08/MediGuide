from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from ..auth.routes import authentication
from ..config.db import reports_collection
from .vector import load_vectorstore, summarize_pdf
import uuid
from datetime import datetime, timezone

router = APIRouter(prefix="/docs", tags=["Documents"])


class DocumentRequest(BaseModel):
    role: str


def save_report_metadata(doc_id: str, filename: str, owner: str, role: str, summary: str, report_type: str):
    reports_collection.insert_one({
        "doc_id": doc_id,
        "filename": filename,
        "owner": owner,
        "role": role,
        "summary": summary,
        "type": report_type,
        "uploaded_at": datetime.now(timezone.utc).isoformat()
    })


@router.post("/")
async def upload_document(
    file: UploadFile = File(...),
    role: str = Form(...),
    user=Depends(authentication)
):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can upload reference documents.")

    doc_id = str(uuid.uuid4())
    save_path = Path("./uploaded_docs") / f"{doc_id}_{file.filename}"
    save_path.parent.mkdir(parents=True, exist_ok=True)

    content = await file.read()
    save_path.write_bytes(content)

    vector_warning = None
    try:
        load_vectorstore(str(save_path), file.filename, role, doc_id)
    except Exception as e:
        vector_warning = str(e)

    save_report_metadata(
        doc_id=doc_id,
        filename=file.filename,
        owner=user["username"],
        role=role,
        summary="",
        report_type="reference"
    )

    response = {
        "message": "Document uploaded successfully",
        "doc_id": doc_id,
        "accessible_to": role
    }
    if vector_warning:
        response["warning"] = f"Vectorization failed: {vector_warning}"
    return response


@router.post("/report")
async def upload_medical_report(
    file: UploadFile = File(...),
    user=Depends(authentication)
):
    if user["role"] != "patient":
        raise HTTPException(status_code=403, detail="Only patients can upload their medical reports.")

    doc_id = str(uuid.uuid4())
    save_path = Path("./uploaded_docs") / f"{doc_id}_{file.filename}"
    save_path.parent.mkdir(parents=True, exist_ok=True)

    content = await file.read()
    save_path.write_bytes(content)

    role = user["role"]

    try:
        summary = summarize_pdf(str(save_path))
    except Exception as e:
        summary = f"[Summarization unavailable] Could not generate summary: {str(e)}"

    vector_warning = None
    try:
        load_vectorstore(str(save_path), file.filename, role, doc_id)
    except Exception as e:
        vector_warning = str(e)

    save_report_metadata(
        doc_id=doc_id,
        filename=file.filename,
        owner=user["username"],
        role=role,
        summary=summary,
        report_type="patient_report"
    )

    response = {
        "message": "Medical report uploaded and summarized successfully.",
        "doc_id": doc_id,
        "role": role,
        "summary": summary
    }
    if vector_warning:
        response["warning"] = f"Vectorization failed: {vector_warning}"
    return response


@router.get("/reports")
def get_reports(user=Depends(authentication)):
    query = {} if user["role"] == "admin" else {"owner": user["username"]}
    documents = list(reports_collection.find(query))
    for doc in documents:
        doc.pop("_id", None)
    return {"reports": documents}


@router.get("/reports/{doc_id}")
def get_report(doc_id: str, user=Depends(authentication)):
    report = reports_collection.find_one({"doc_id": doc_id})
    if not report:
        return {"error": "Report not found"}

    if user["role"] != "admin" and report["owner"] != user["username"]:
        return {"error": "Access denied"}

    report.pop("_id", None)
    return report
