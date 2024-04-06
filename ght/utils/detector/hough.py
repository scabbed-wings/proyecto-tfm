import numpy as np
import matplotlib.pyplot as plt
import cv2 

def ght_det(im, mode, alg):
    guil = True if alg == "guil" else False
    #scale = 0.8
    #new_shape = (int(im.shape[0] * scale), int(im.shape[1] * scale))
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    #gray = cv2.resize(gray, new_shape)
    #img_res = cv2.resize(im, new_shape)
    
    canny_im = cv2.Canny(gray, 10, 50)
    temp = 0

    if mode == "r":
        temp = cv2.imread("utils/detector/rect.png", cv2.IMREAD_GRAYSCALE)
    elif mode == "e":
        temp = cv2.imread("utils/detector/ellipse2.png", cv2.IMREAD_GRAYSCALE)
    else:
        temp = cv2.imread("utils/detector/rhombus.png", cv2.IMREAD_GRAYSCALE)
    
    #scale = 0.5
    #new_shape = (int(temp.shape[0] * scale), int(temp.shape[1] * scale))
    #temp.resize(new_shape)
    #print(temp.shape)
    #plt.imshow(temp, cmap='gray')
    #plt.show()
    if guil:
        det = cv2.createGeneralizedHoughGuil()
        det.setMinDist(10)
        det.setLevels(90)
        det.setDp(2)
        det.setMaxBufferSize(1000)
        det.setCannyLowThresh(10)
        det.setCannyHighThresh(50)
    else:
        det = cv2.createGeneralizedHoughBallard()
        det.setMinDist(10)
        det.setLevels(90)
        det.setDp(1)
        det.setMaxBufferSize(1000)
        det.setCannyLowThresh(10)
        det.setCannyHighThresh(50)
    
    det.setTemplate(temp)

    pos, votes = det.detect(canny_im)
    #print("Pos: ", pos, " Votes: ", votes)
    for i in range(pos.shape[1]):
        if votes[0][i][0] > 300:
            pos_xy = pos[0][i][0:2]
            sc = pos[0][i][2]
            angle = pos[0][i][3]
            rrect = cv2.RotatedRect(pos_xy, np.array([temp.shape[1], temp.shape[0]]) * sc, angle)
            pts = rrect.points()
            if guil:
                cv2.line(im, np.int16((pts[0,:])), np.int16(pts[1,:]), (0, 0, 255), 2)
                cv2.line(im, np.int16((pts[1,:])), np.int16(pts[2,:]), (0, 0, 255), 2)
                cv2.line(im, np.int16((pts[2,:])), np.int16(pts[3,:]), (0, 0, 255), 2)
                cv2.line(im, np.int16((pts[3,:])), np.int16(pts[0,:]), (0, 0, 255), 2)
            else:
                cv2.polylines(im, np.int32([pts]), False, (0, 0, 255), 2)
            rect = rrect.boundingRect()
            cv2.rectangle(im, rect[0:2], rect[2:], (0, 0, 255), 2 )
    
    plt.imshow(im, cmap='gray')
    plt.show()