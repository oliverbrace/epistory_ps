import cv2


def get_contours(image):
    contours, hierarchy = cv2.findContours(
        image=image, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
    return contours


def get_rectangles_from_contours(contours, min_size):
    """_summary_

    Args:
        contours (List): List of contour to be passed_

    Returns:
        _type_: List of [xStart, yStart, width, height]
    """
    rectangles = []
    for c in contours:
        area = cv2.contourArea(c)
        if area > min_size and area < 1000000:
            new_rect = cv2.boundingRect(c)
            if (new_rect[3] > 25 and new_rect[2] > 15):
                rectangles.append(new_rect)

    return rectangles


def draw_rectangle(image, rectangle, colour=(0, 255, 0), thickness=-1):
    """_summary_

    Args:
        rect (_type_): list with [xStart, yStart, width, height]
        image (_type_): Colour image to draw on
        colour (tuple): 
    """
    image_copy = image.copy()

    xStart = int(rectangle[0])
    xEnd = int((rectangle[0]+rectangle[2]))
    yStart = int(rectangle[1])
    yEnd = int((rectangle[1]+rectangle[3]))

    return cv2.rectangle(image_copy, (xStart, yStart),
                         (xEnd, yEnd), colour, thickness)


def find_rectangles(img_to_contour, min_size=200):
    """_summary_

    Args:
        img_to_contour (_type_): _description_
        min_size (int, optional): _description_. Defaults to 200.

    Returns:
        _type_: List of [xStart, yStart, width, height]
    """
    contours = get_contours(img_to_contour)
    return get_rectangles_from_contours(contours, min_size)


def draw_contours(image, contours):
    return cv2.drawContours(image=image, contours=contours,
                            contourIdx=-1, color=(0, 255, 0), thickness=2)


def find_and_draw_rectangles(img_to_contour, img_to_draw_on, min_size=200):
    """_summary_

    Args:
        img_to_contour (_type_): Image to detect contours
        img_to_draw_on (_type_): Colour image to be drawn on

    Returns:
        _type_: _description_
    """

    rectangles = find_rectangles(img_to_contour, min_size)

    # rectangles, weights = cv2.groupRectangles(rectangles, 1, 5)

    for rect in rectangles:
        img_to_draw_on = draw_rectangle(
            img_to_draw_on, rect, colour=(0, 255, 0), thickness=2)

    return img_to_draw_on
