"""
FastAPI entrypoint exposing a healthcheck and an endpoint
to convert HTML content into a PDF file using wkhtmltopdf.
"""

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

from .utils import convert_html_to_pdf


class HtmlPayload(BaseModel):
    """
    Request body model for HTML to PDF conversion.
    """

    html: str


app = FastAPI()


@app.get("/health")
def healthcheck():
    return {"status": "ok"}


@app.post("/html-to-pdf")
def html_to_pdf(payload: HtmlPayload) -> Response:
    """
    Convert provided HTML content to a PDF binary response.
    """
    try:
        pdf_bytes = convert_html_to_pdf(payload.html)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename=\"document.pdf\"'},
    )
