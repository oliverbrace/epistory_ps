import cv2
import numpy as np
from misc_func import num_channels_check


def invert_black_white(image):
    return cv2.bitwise_not(image)


def create_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def gray_to_bl(image, thresh=2):
    """_summary_

    Args:
        gray_image (_type_): Grey scale image
        thresh (_type_): _description_

    Returns:
        _type_: Black and white image
    """

    channels = num_channels_check(image)
    if (channels > 2):
        raise Exception("Image is not grey")

    (_, bl_image) = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)
    return bl_image


def opening(image, thresh):
    """erosion followed by dilation - removes noise

    Args:
        image (_type_): _description_
        thresh (_type_): _description_

    Returns:
        _type_: _description_
    """
    kernel = np.ones((thresh, thresh), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


def closing(image, thresh=2):
    """ dilation followed by erosion - fills in gaps

    Args:
        image (_type_): _description_
        thresh (_type_): _description_

    Returns:
        _type_: _description_
    """
    kernel = np.ones((thresh, thresh), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)


def crop_image(image, xStart, xEnd, yStart, yEnd):
    return image[yStart:yEnd, xStart:xEnd]


def generate_mask(image, lower, upper):
    if (lower is None or upper is None):
        raise Exception("Lower or Upper not set")

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    return gray_to_bl(mask, 254)


def apply_mask(image, mask):
    if (mask == None):
        raise Exception("No mask")

    return cv2.bitwise_and(image, image, mask=mask)


def ice_filter_mask(image):
    lower = np.array([80, 160, 245])
    upper = np.array([100, 220, 255])
    return generate_mask(image, lower, upper)


def normal_filter_mask(image):
    lower = np.array([0, 0, 254])
    upper = np.array([10, 10, 255])
    return generate_mask(image, lower, upper)


def apply_mask(image, mask):
    return cv2.bitwise_and(image, image, mask=mask)
