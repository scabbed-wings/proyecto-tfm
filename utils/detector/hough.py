import numpy as np
import matplotlib.pyplot as plt
import cv2 

def ght_det(im, mode):
    canny_im = cv2.Canny(im, 100, 200)
    if mode == "s":
        ght_rect(canny_im)
    elif mode == "e":
        ght_ellipse(canny_im)
    else:
        ght_rhombus(canny_im)


def ght_rect(im):
    pass


def ght_ellipse(im):
    pass


def ght_rhombus(im):
    pass
