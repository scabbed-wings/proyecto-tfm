import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def read_box(image, box):
    crop = image.crop(tuple(box.int().tolist()))
    crop = crop.convert('L')
    array_im = np.array(crop)
    text = pytesseract.image_to_string(array_im, lang='spa', config='--psm 4 --oem 1 --dpi 300')
    return text
