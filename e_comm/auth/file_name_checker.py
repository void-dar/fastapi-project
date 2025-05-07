import os
import uuid
import shutil
from fastapi import UploadFile, HTTPException

# Define allowed extensions for images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def secure_filename(filename: str) -> str:
    """
    Sanitizes the filename to ensure it's safe and remove any special characters.
    """
    return filename.replace(" ", "_").replace("..", "")

def validate_extension(filename: str) -> bool:
    """
    Check if the file extension is allowed.
    """
    return filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS

async def upload_product_image(file: UploadFile):
    # Ensure the upload directory exists
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    # Sanitize the filename
    filename = secure_filename(file.filename)

    # Validate file extension
    if not validate_extension(filename):
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Generate a unique filename using UUID
    unique_filename = f"{uuid.uuid4()}_{filename}"
    
    # Save the file
    file_path = os.path.join(upload_dir, unique_filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)  # Efficient file writing

    # Return the file path or store it in the database
    return file_path
