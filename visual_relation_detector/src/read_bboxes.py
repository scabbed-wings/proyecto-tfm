import pytesseract
import numpy as np
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def read_boxes(image, boxes):
    boxes_list = boxes.int().tolist()
    for box in boxes_list:
        crop = image.crop(tuple(box))
        crop = crop.convert('L')
        array_im = np.array(crop)
        text = pytesseract.image_to_string(array_im, lang='spa', config='--psm 4 --oem 1 --dpi 300')
        plt.subplot(1, 2, 1)
        plt.axis('off')
        plt.imshow(array_im, 'gray')
        plt.subplot(1, 2, 2)
        plt.axis('off')
        zeros = np.ones([200, 200])
        plt.imshow(zeros, 'gray', vmin=0, vmax=1)
        plt.text(70, 100, text, fontsize=15)
        plt.show()
