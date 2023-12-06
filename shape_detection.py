import cv2
from glob import glob

file_list = glob("img/*.png")
for elem in file_list[:4]:
    img = cv2.imread(elem)
    
    scale = 0.8
    new_shape = (int(img.shape[0] * scale), int(img.shape[1] * scale))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, new_shape)
    img_res = cv2.resize(img, new_shape)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_OTSU)
    cont, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for elem in cont[1:]:
        poly_approx = cv2.approxPolyDP(elem, 0.01 * cv2.arcLength(elem, True), True)
        cv2.drawContours(img_res, [elem], 0, (0, 0, 255), 1)
    

    cv2.imshow("Img",thresh)
    cv2.waitKey(0)