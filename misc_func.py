import cv2
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


def num_channels_check(img):
    return img.ndim


def rgb_to_hsv_colour(r, g, b):
    rgb = np.uint8([[[r, g, b]]])
    return cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)


def read_image(file_name, change=True, path="epi_screenshots"):
    # IMREAD_UNCHANGED needed to keep number of channels the same
    return cv2.imread(f"{path}/{file_name}", cv2.IMREAD_UNCHANGED if change else None)


def save_image(file_name, img, path="epi_screenshots"):
    # example cv2.imwrite('test_gray.jpg', gray)
    cv2.imwrite(f"{path}/{file_name}.png", img)


def find_imgs_diff(img1, img2, openCV=True):
    if (openCV):
        return cv2.subtract(img1, img2)
    else:
        # (score, diff) = compare_ssim(img1, img2, full=True)
        # return (diff * 255).astype("uint8")
        return


def find_text_in_image(image):
    custom_config = r"-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 8"
    return pytesseract.image_to_string(image, config=custom_config)
