import pytesseract
from PIL import Image

def read_meter(image_file):
    img = Image.open(image_file)
    text = pytesseract.image_to_string(img, config="--psm 7 digits")
    try:
        value = float("".join([c for c in text if c.isdigit() or c=="."]))
    except:
        value = None
    return value
