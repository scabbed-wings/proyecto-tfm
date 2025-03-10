import numpy as np
import cv2
import matplotlib.pyplot as plt
from collections import defaultdict


def hough_grad(gray):
    dx = cv2.Sobel(gray, cv2.CV_32F, dx=1, dy=0, ksize=5)
    dy = cv2.Sobel(gray, cv2.CV_32F, dx=0, dy=1, ksize=5)
    grad = np.arctan2(dy, dx) * 180 / np.pi

    # plt.clf()
    # fig = plt.figure()
    # fig.add_subplot(1,3,1)
    # plt.title("DX")
    # plt.imshow(dx)

    # fig.add_subplot(1,3,2)
    # plt.title("DY")
    # plt.imshow(dy)

    # fig.add_subplot(1,3,3)
    # plt.title("Gradient")
    # plt.imshow(grad)

    # plt.show()
    return grad


def r_table(canny, centre):
    grad = hough_grad(canny)
    r_table = defaultdict(list)
    for (i, j), value in np.ndenumerate(canny):
        if value:
            r = (centre[0] - i, centre[1] - j)
            ind = grad[i, j]
            # print((i,j), " Valor: ", value, " Gradiente: ", grad[i, j])
            r_table[ind].append(r)
    return r_table


def accum_grads(r_t, canny):
    accum = np.zeros(canny.shape)
    grad = hough_grad(canny)
    for (i, j), value in np.ndenumerate(canny):
        if value:
            ind = grad[i, j]
            for r in r_t[ind]:
                accum_i, accum_j = int(i + r[0]), int(j + r[1])
                if accum_i < accum.shape[0] and accum_j < accum.shape[1]:
                    # print("Accum_i:", accum_i, " Accum_j: ", accum_j)
                    accum[accum_i, accum_j] += 1

    return accum


def n_max(mat, n):
    ind = mat.ravel().argsort()[-n:]
    ind = (np.unravel_index(i, mat.shape) for i in ind)
    # print([(mat[i], i) for i in ind])
    return [(mat[i], i) for i in ind]


def threshold_accum(accum, threshold):
    valid_positions = list()
    for i in range(accum.shape[0]):
        for j in range(accum.shape[1]):
            votes = accum[i][j]
            if votes >= threshold:
                valid_positions.append((votes, (i, j)))
    return valid_positions


def hough_closure(im, temp):
    gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    gray_temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
    canny_im = cv2.Canny(gray_im, 10, 50)
    canny_temp = cv2.Canny(gray_temp, 10, 50)
    centre = (gray_temp.shape[0]/2, gray_temp.shape[1]/2)

    kernel = np.ones((3, 3), np.uint8)
    canny_im = cv2.morphologyEx(canny_im, cv2.MORPH_CROSS, kernel)

    r = r_table(canny_temp, centre)
    accum = accum_grads(r, canny_im)
    return accum


def create_fig(temp, im_s, accum, top_points=True):
    plt.clf()

    plt.figure(0)
    plt.title("Plantilla")
    plt.gray()
    plt.imshow(temp)

    plt.figure(1)
    # plt.title("Imagen de busqueda")
    plt.axis('off')
    plt.gray()
    plt.imshow(im_s)

    plt.figure(2)
    # plt.title("Acumulador")
    plt.axis('off')
    plt.imshow(accum, cmap='hot', norm='linear', aspect=1)

    plt.figure(3)
    # plt.title("Deteccion")
    plt.axis('off')
    plt.gray()
    plt.imshow(im_s)

    if top_points:
        top = n_max(accum, 150)
    else:
        top = threshold_accum(accum, 200)

    y_points = [pt[1][1] for pt in top]
    x_points = [pt[1][0] for pt in top]

    plt.scatter(y_points, x_points, marker='o', color='r')
    plt.show()


def create_templates(paths):
    temp_list = []
    for elem in paths:
        new_temp = cv2.imread(elem)
        temp_list.append(new_temp)
    return temp_list


def test_hough(temp_list, im_path):
    im = cv2.imread(im_path)
    # princ_accum = np.zeros(im.shape[:-1])
    for temp_path in temp_list:
        temp = cv2.imread(temp_path)
        accum = hough_closure(im, temp)
        # princ_accum += accum
        create_fig(temp, im, accum)


if __name__ == "__main__":
    # path_im = r"deep_learning\prueba.png"
    path_im = "data_generator/test/img340.png"
    paths_temp = ["ght/utils/detector/ellipse_xl.png", "ght/utils/detector/ellipse2.png", "ght/utils/detector/ellipse.png"]
    # paths_temp = [r"ght\utils\detector\ellipse.png", "ght/utils/detector/rhombus.png", r"ght\utils\detector\rect.png"]
    # paths_temp = [r"ght\utils\detector\ellipse.png"]
    test_hough(paths_temp, path_im)
