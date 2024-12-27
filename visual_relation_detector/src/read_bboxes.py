import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def read_boxes(image, boxes):
    boxes_list = boxes.int().tolist()
    for box in boxes_list:
        crop = image.crop(tuple(box))
        crop = crop.convert('L')
        array_im = np.array(crop)
        text = pytesseract.image_to_string(array_im, lang='spa', config='--psm 4 --oem 1 --dpi 300')
        print(text)
    # return text
