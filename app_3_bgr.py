from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
import io

app = FastAPI()

@app.post("/remove_background")
async def remove_background(file: UploadFile = File(...)):
    try:
        # Read file
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        # Remove background and set a white background
        output = remove(image, bgcolor=[255, 255, 255, 255])

        # Convert RGBA to RGB
        rgb_output = output.convert("RGB")

        # Save the processed image to a BytesIO object
        img_io = io.BytesIO()
        rgb_output.save(img_io, format='JPEG')
        img_io.seek(0)

        # Return the processed image directly as a response
        return StreamingResponse(img_io, media_type="image/jpeg")

    except Exception as e:
        return {"error": str(e)}