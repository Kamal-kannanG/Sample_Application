from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
from typing import Optional
import os
import mimetypes
import fitz  # PyMuPDF
import docx

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/upload")
async def upload(
    request: Request,
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None)
):
    extracted_text = None
    # If file is provided, prioritize it
    if file:
        filename = file.filename
        content_type = file.content_type or mimetypes.guess_type(filename)[0]
        ext = os.path.splitext(filename)[1].lower()
        file_bytes = await file.read()
        if ext == ".pdf" or (content_type and "pdf" in content_type):
            # PDF extraction
            try:
                with fitz.open(stream=file_bytes, filetype="pdf") as doc:
                    extracted_text = "".join(page.get_text() for page in doc)
            except Exception as e:
                return JSONResponse(status_code=400, content={"error": f"PDF extraction failed: {str(e)}"})
        elif ext == ".docx" or (content_type and "word" in content_type):
            # DOCX extraction
            try:
                from io import BytesIO
                doc = docx.Document(BytesIO(file_bytes))
                extracted_text = "\n".join([p.text for p in doc.paragraphs])
            except Exception as e:
                return JSONResponse(status_code=400, content={"error": f"DOCX extraction failed: {str(e)}"})
        elif ext == ".md" or (content_type and "markdown" in content_type):
            # Markdown extraction
            try:
                extracted_text = file_bytes.decode("utf-8")
            except Exception as e:
                return JSONResponse(status_code=400, content={"error": f"Markdown extraction failed: {str(e)}"})
        else:
            return JSONResponse(status_code=400, content={"error": "Unsupported file type. Only PDF, DOCX, and MD are allowed."})
    else:
        # Try to get text from form or JSON
        if request.headers.get("content-type", "").startswith("application/json"):
            data = await request.json()
            extracted_text = data.get("text")
        else:
            extracted_text = text
    if not extracted_text:
        return JSONResponse(status_code=400, content={"error": "No text or supported file provided."})
    return {"extracted_text": extracted_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
