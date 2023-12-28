import cv2
from glob import glob
import utils.detector.hough as H
import matplotlib.pyplot as plt

file_list = glob("img/*.png")
alg = "bal"
for elem in file_list[:4]:
    img = cv2.imread(elem)
    

    # Uso de contornos y umbralizado para la detección de formas
    #_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_OTSU)
    #cont, hier = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #newborns = []
    #for ind, elem in enumerate(cont[1:]):
    #    
    #    # Hierarchy [Next, Previous, First_Child, Parent]
    #    #poly_approx = cv2.approxPolyDP(elem, 0.01 * cv2.arcLength(elem, True), True)
    #    if hier[0][ind][3] == 0:
    #        print("Hierarchy: ", hier[0][ind], "Len contour ", len(elem))
    #        cv2.drawContours(img_res, [elem], 0, (0, 0, 255), 1)
    #cv2.imshow("Img",img_res)
    #cv2.waitKey(0)

H.ght_det(img, "r", alg)
#H.ght_det(img, "e")
#H.ght_det(img, "rh")
