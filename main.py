from fastapi import FastAPI, File, UploadFile, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from pyzbar.pyzbar import decode
from PIL import Image
import io
import os

# In a real production environment, this should be stored in an environment variable
API_KEY = os.getenv("SCANNER_API_KEY", "my-super-secret-key")
API_KEY_NAME = "X-API-Key"

app = FastAPI(title="Barcode & QR Code Scanner API")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def validate_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    raise HTTPException(
        status_code=403,
        detail="Could not validate credentials. Invalid API Key.",
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to the Barcode & QR Code Scanner API. Use the /scan endpoint to upload an image."}

@app.post("/scan")
async def scan_barcode(file: UploadFile = File(...), api_key: str = Depends(validate_api_key)):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Read the image content
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Decode barcodes and QR codes
        decoded_objects = decode(image)

        if not decoded_objects:
            return {"message": "No barcode or QR code detected in the image.", "data": []}

        results = []
        for obj in decoded_objects:
            results.append({
                "type": obj.type,
                "data": obj.data.decode("utf-8"),
                "rect": {
                    "left": obj.rect.left,
                    "top": obj.rect.top,
                    "width": obj.rect.width,
                    "height": obj.rect.height
                }
            })

        return {"message": f"Successfully detected {len(results)} barcode(s)/QR code(s).", "data": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)