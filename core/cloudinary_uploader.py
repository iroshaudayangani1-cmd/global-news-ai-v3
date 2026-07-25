import cloudinary
import cloudinary.uploader

from config.settings import (
    CLOUDINARY_CLOUD_NAME,
    CLOUDINARY_API_KEY,
    CLOUDINARY_API_SECRET,
)

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True,
)


def upload_image(image_path):

    result = cloudinary.uploader.upload(
        image_path,
        folder="global-viral-report",
    )

    return result["secure_url"]
