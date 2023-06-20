import cv2
import numpy as np

input_fn = "Demo/00001_input.jpg"


def my_guidedFilter_oneChannel(srcImg, guidedImg, rad=9, eps=1e-8):
    srcImg = srcImg / 255.0
    guidedImg = guidedImg / 255.0
    img_shape = np.shape(srcImg)

    P_mean = cv2.boxFilter(srcImg, -1, (rad, rad), normalize=True)
    I_mean = cv2.boxFilter(guidedImg, -1, (rad, rad), normalize=True)

    I_square_mean = cv2.boxFilter(np.multiply(guidedImg, guidedImg), -1, (rad, rad), normalize=True)
    I_mul_P_mean = cv2.boxFilter(np.multiply(srcImg, guidedImg), -1, (rad, rad), normalize=True)

    var_I = I_square_mean - np.multiply(I_mean, I_mean)
    cov_I_P = I_mul_P_mean - np.multiply(I_mean, P_mean)

    a = cov_I_P / (var_I + eps)
    b = P_mean - np.multiply(a, I_mean)

    a_mean = cv2.boxFilter(a, -1, (rad, rad), normalize=True)
    b_mean = cv2.boxFilter(b, -1, (rad, rad), normalize=True)

    dstImg = np.multiply(a_mean, guidedImg) + b_mean

    return dstImg * 255.0


def my_guidedFilter_threeChannel(srcImg, guidedImg, rad=9, eps=0.01):
    img_shape = np.shape(srcImg)

    dstImg = np.zeros(img_shape, dtype=float)

    for ind in range(0, img_shape[2]):
        dstImg[:, :, ind] = my_guidedFilter_oneChannel(srcImg[:, :, ind],
                                                       guidedImg[:, :, ind], rad, eps)

    dstImg = dstImg.astype(np.uint8)

    return dstImg


def main():
    img = cv2.imread(input_fn)
    print(np.shape(img))

    dstimg = my_guidedFilter_threeChannel(img, img, 15, 1)
    print(np.shape(dstimg))
    cv2.imshow('base', dstimg)
    cv2.waitKey(0)
    cv2.imwrite('Demo/00001_base.jpg', dstimg)
    detail = img - dstimg
    cv2.imshow('detail', detail)
    cv2.waitKey(0)
    cv2.imwrite('Demo/00001_detail.jpg', detail)


if __name__ == '__main__':
    main()
