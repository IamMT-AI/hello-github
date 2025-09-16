"""
2D Stylization Service
Addresses the cartoonize-service draft issue.
MVP Week 1: Placeholder FastAPI service returning dummy Base64 image with latency simulation.
"""

import asyncio
import base64
import time
from io import BytesIO
from typing import Dict, Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image

app = FastAPI(
    title="2D Stylization Service",
    description="MVP Week 1 - Placeholder service for 2D cartoon stylization",
    version="0.1.0",
)

# Dummy 1x1 transparent PNG as placeholder
PLACEHOLDER_IMAGE_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="


def create_dummy_stylized_image(original_size: tuple = (256, 256)) -> str:
    """Create a dummy stylized image placeholder"""
    # Create a simple colored rectangle as placeholder
    img = Image.new("RGB", original_size, color=(255, 182, 193))  # Light pink

    # Add some simple pattern to make it look "stylized"
    pixels = img.load()
    for x in range(0, original_size[0], 20):
        for y in range(original_size[1]):
            if pixels and x < original_size[0]:
                pixels[x, y] = (255, 105, 180)  # Hot pink stripes

    # Convert to base64
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()
    return base64.b64encode(img_bytes).decode()


async def simulate_stylization_processing(
    processing_complexity: float = 1.0,
) -> Dict[str, Any]:
    """Simulate stylization processing with realistic latency"""
    # Simulate processing time (0.5-2.0 seconds based on complexity)
    processing_time = 0.5 + (processing_complexity * 1.5)
    await asyncio.sleep(processing_time)

    return {
        "processing_time": processing_time,
        "model_version": "sdxl-placeholder-v1",
        "style": "cartoon-2d",
    }


@app.get("/")
async def root():
    """Service health check"""
    return {
        "service": "2D Stylization Service",
        "status": "running",
        "version": "0.1.0-mvp",
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "model_loaded": False,  # Will be true when real model is integrated
        "gpu_available": False,  # Will check GPU availability when model is added
        "processing_queue": 0,
    }


@app.post("/stylize")
async def stylize_image(file: UploadFile = File(...)):
    """
    Stylize an uploaded image into 2D cartoon style.

    MVP Week 1: Returns placeholder stylized image with timing simulation.
    """
    start_time = time.time()

    try:
        # Validate image
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(status_code=400, detail="Empty file")

        # Parse image to get dimensions
        try:
            img = Image.open(BytesIO(contents))
            original_size = img.size
            img_format = img.format
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image: {str(e)}")

        # Simulate processing complexity based on image size
        complexity = min(2.0, (original_size[0] * original_size[1]) / (512 * 512))

        # Simulate stylization processing
        processing_result = await simulate_stylization_processing(complexity)

        # Generate dummy stylized image
        stylized_b64 = create_dummy_stylized_image(original_size)

        total_time = time.time() - start_time

        return {
            "status": "success",
            "message": "Image stylized successfully (placeholder)",
            "original_info": {
                "filename": file.filename,
                "size": len(contents),
                "dimensions": original_size,
                "format": img_format,
            },
            "stylized_image": f"data:image/png;base64,{stylized_b64}",
            "processing_info": processing_result,
            "timing": {
                "total_time": total_time,
                "processing_time": processing_result["processing_time"],
                "overhead_time": total_time - processing_result["processing_time"],
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stylization failed: {str(e)}")


@app.get("/models")
async def list_models():
    """List available stylization models"""
    return {
        "available_models": [
            {
                "name": "sdxl-placeholder-v1",
                "description": "Placeholder model for MVP Week 1",
                "status": "active",
                "type": "placeholder",
            }
        ],
        "default_model": "sdxl-placeholder-v1",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8001, reload=True)
