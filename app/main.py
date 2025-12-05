# FastAPI app exposing a health check and a stub HTML to PDF conversion endpoint
from io import BytesIO

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from .utils import convert_html_to_pdf


class HtmlPayload(BaseModel):
    html: str


app = FastAPI()


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/convert")
def convert(payload: HtmlPayload) -> StreamingResponse:
    try:
        pdf_bytes = convert_html_to_pdf(payload.html)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="PDF conversion failed",
        )

    pdf_stream = BytesIO(pdf_bytes)
    pdf_stream.seek(0)

    return StreamingResponse(
        pdf_stream,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=document.pdf"},
    )
