import os
from PIL import Image
from django.core.exceptions import ValidationError


def validate_image_upload(
    image_file,
    max_size_mb=2,
    min_width=100,
    min_height=100,
    max_width=2000,
    max_height=2000,
    target_aspect_ratio=1.0,
    aspect_ratio_tolerance=0.20,
    allowed_formats=('JPEG', 'PNG', 'WEBP')
):
    """
    Validate uploaded image for file size, valid image data, format,
    dimensions, and aspect ratio.

    Returns:
        tuple (is_valid: bool, error_message: str or None)
    """
    if not image_file:
        return False, "No image file was provided."

    # 1. File size limit
    max_bytes = max_size_mb * 1024 * 1024
    if image_file.size > max_bytes:
        uploaded_mb = image_file.size / (1024 * 1024)
        return False, (
            f"Image file size is too large ({uploaded_mb:.2f} MB). "
            f"The maximum allowed size is {max_size_mb} MB."
        )

    # 2. File format verification via Pillow
    try:
        image_file.seek(0)
        img = Image.open(image_file)
        img.verify()
    except Exception:
        return False, "The uploaded file is not a valid or readable image. Please upload a standard PNG, JPG, or WebP image."

    # Re-open after verify() to inspect properties (verify closes internal pointer)
    try:
        image_file.seek(0)
        img = Image.open(image_file)
    except Exception:
        return False, "Unable to inspect image properties. Please re-save the image and try again."

    img_format = (img.format or '').upper()
    if img_format not in allowed_formats:
        allowed_str = ", ".join(allowed_formats)
        return False, f"Unsupported image format '{img_format}'. Allowed formats are: {allowed_str}."

    # 3. Dimensions validation
    width, height = img.size
    if width < min_width or height < min_height:
        return False, (
            f"Image dimensions are too small ({width}x{height}px). "
            f"Minimum required dimensions are {min_width}x{min_height}px."
        )

    if width > max_width or height > max_height:
        return False, (
            f"Image dimensions are too large ({width}x{height}px). "
            f"Maximum allowed dimensions are {max_width}x{max_height}px."
        )

    # 4. Aspect ratio validation (default 1:1 Square)
    if target_aspect_ratio is not None and height > 0:
        ratio = width / height
        lower_bound = target_aspect_ratio - aspect_ratio_tolerance
        upper_bound = target_aspect_ratio + aspect_ratio_tolerance
        if not (lower_bound <= ratio <= upper_bound):
            return False, (
                f"Image must have an approximate 1:1 square aspect ratio. "
                f"Uploaded image is {width}x{height}px (ratio {ratio:.2f}:1). "
                f"Please crop the image to a square before uploading."
            )

    image_file.seek(0)
    return True, None

