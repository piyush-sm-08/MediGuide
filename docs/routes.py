from fastapi import APIRouter,Depends,UploadFile,File,Form,HTTPException
from auth.routes import authentication
from .vector import load_vectorstore
import uuid

router = APIRouter()

@router.post("/upload_docs")
def upload_docs(
    user = Depends(authentication),
    file:UploadFile=File(...),
    role:str=Form(...)
):
    if user["role"] != "admin":
        raise HTTPException(status_code = 403 , details="Only admin can upload files")
    
    doc_id = str(uuid.uuid4())
    load_vectorstore([file],role,doc_id)
    return {"message" : f"{file.filename} uploaded successfully" , "doc_id":doc_id , "accessible_to" : role}
