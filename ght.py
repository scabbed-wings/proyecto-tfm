import numpy as np
import cv2
import matplotlib.pyplot as plt
from collections import defaultdict

def hough_grad(gray):
    dx = cv2.Sobel(gray, cv2.CV_32F, dx=1, dy=0, ksize=5)
    dy = cv2.Sobel(gray, cv2.CV_32F, dx=0, dy=1, ksize=5)
    grad = np.arctan2(dy, dx) +  np.pi

    plt.clf()
    fig = plt.figure()
    fig.add_subplot(1,3,1)
    plt.title("DX")
    plt.imshow(dx)
    

    fig.add_subplot(1,3,2)
    plt.title("DY")
    plt.imshow(dy)

    fig.add_subplot(1,3,3)
    plt.title("Gradient")
    plt.imshow(grad)

    plt.show()
    return grad

def r_table(canny, centre):
    grad = hough_grad(canny)
    r_table = defaultdict(list)
    for (i, j), value in np.ndenumerate(canny):
        if value:
            r = np.sqrt(((centre[0] - i) ** 2) + (centre[1] - j) ** 2)
            alpha = np.arctan2(i - centre[0], j - centre[1]) + np.pi
            ind = grad[i,j] / (2 * np.pi)
            # print((i,j), " Valor: ", value, " Gradiente: ", grad[i, j])
            r_table[ind].append((r, alpha))
    return r_table

def accum_grads(r_t, canny):
    accum = np.zeros(canny.shape)
    grad = hough_grad(canny)
    for (i,j), value in np.ndenumerate(canny):
        if value:
            ind = grad[i,j] / (2 * np.pi)
            for r, alpha in r_t[ind]:
                accum_i, accum_j = int(i + r * np.sin(alpha)), int(j + r * np.cos(alpha))
                if accum_i < accum.shape[0] and accum_j < accum.shape[1]:
                    #print("Accum_i:", accum_i, " Accum_j: ", accum_j)
                    accum[accum_i, accum_j] += 1
    
    return accum

def n_max(mat, n):
    ind = mat.ravel().argsort()[-n:]
    ind = (np.unravel_index(i, mat.shape) for i in ind)
    return [(mat[i], i) for i in ind]

def hough_closure(im, temp):
    gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    gray_temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
    canny_im = cv2.Canny(gray_im, 10, 50)
    canny_temp = cv2.Canny(gray_temp, 10, 50)
    centre = (gray_im.shape[0]/2, gray_im.shape[1]/2)
    
    r = r_table(canny_temp, centre)
    accum = accum_grads(r, canny_im)
    return accum

def create_fig(temp, im_s, accum):
    plt.clf()
    plt.gray()

    fig = plt.figure()
    fig.add_subplot(2, 2, 1)
    plt.title("Plantilla")
    plt.imshow(temp)

    fig.add_subplot(2,2,2)
    plt.title("Imagen de busqueda")
    plt.imshow(im_s)

    fig.add_subplot(2,2,3)
    plt.title("Acumulador")
    plt.imshow(accum)

    fig.add_subplot(2,2,4)
    plt.title("Deteccion")
    plt.imshow(im_s)

    top = n_max(accum, 50)

    # print(top)

    y_points = [pt[1][0] for pt in top]
    x_points = [pt[1][1] for pt in top]
    plt.scatter(y_points, x_points, marker='o', color='r')
    plt.show()

def test_hough(temp_path, im_path):
    im = cv2.imread(im_path)
    temp = cv2.imread(temp_path)
    accum = hough_closure(im, temp)

    create_fig(temp, im, accum)


if __name__ == "__main__":
    path_im = "img/img1.png"
    path_temp = "utils/detector/ellipse2.png"
    test_hough(path_temp, path_im)
    
       
    # plt.imshow(grad, cmap='gray')
    # plt.show()

