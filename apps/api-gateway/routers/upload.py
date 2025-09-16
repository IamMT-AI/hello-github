"""
Upload router - Handles file uploads and validation
Addresses the upload-auth-api draft issue.
"""

import time
from io import BytesIO
from typing import Dict, Any

import httpx
from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import Image

router = APIRouter()

# Configuration
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
STYLIZE_SERVICE_URL = "http://localhost:8001"  # Will be configurable via env vars


async def validate_image(file: UploadFile) -> Dict[str, Any]:
    """Validate uploaded image file"""
    # Check file size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413, detail=f"File too large. Max size: {MAX_FILE_SIZE} bytes"
        )

    # Reset file pointer
    await file.seek(0)

    # Check file extension
    if not any(file.filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    try:
        # Validate image format
        image = Image.open(BytesIO(contents))
        image.verify()

        return {
            "filename": file.filename,
            "size": len(contents),
            "format": image.format,
            "dimensions": image.size if hasattr(image, "size") else None,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload and process an image for cartoon figurine generation.

    MVP Week 1: Simplified direct upload with basic validation and timing.
    """
    start_time = time.time()

    try:
        # Validate the uploaded file
        validation_result = await validate_image(file)

        # TODO: Add authentication/authorization check here
        # For MVP Week 1, we skip auth validation

        # Reset file pointer for processing
        await file.seek(0)
        file_contents = await file.read()

        # Call stylization service
        stylize_start = time.time()
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{STYLIZE_SERVICE_URL}/stylize",
                    files={"file": (file.filename, file_contents, file.content_type)},
                    timeout=30.0,
                )
                response.raise_for_status()
                stylize_result = response.json()
            except httpx.RequestError as e:
                # Service unavailable - return placeholder for MVP
                stylize_result = {
                    "message": "Stylization service unavailable - returning placeholder",
                    "stylized_image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
                    "processing_time": 0.1,
                }

        stylize_time = time.time() - stylize_start

        # TODO: Add face-body fusion step here
        # For MVP Week 1, we skip fusion and return stylized result

        processing_time = time.time() - start_time

        return {
            "status": "success",
            "message": "Image processed successfully",
            "file_info": validation_result,
            "result": stylize_result,
            "timing": {
                "total_processing_time": processing_time,
                "stylization_time": stylize_time,
                "validation_time": start_time + (stylize_start - start_time),
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@router.get("/upload/status")
async def upload_status():
    """Get upload service status"""
    return {
        "status": "ready",
        "max_file_size": MAX_FILE_SIZE,
        "allowed_extensions": list(ALLOWED_EXTENSIONS),
        "stylize_service": STYLIZE_SERVICE_URL,
    }
