from email.mime import image
import math
import keyboard
from time import time, sleep


import numpy as np
from image_mod import closing, crop_image, ice_filter_mask, invert_black_white, normal_filter_mask, opening
from misc_func import find_text_in_image, read_image, save_image
from shape_func import draw_contours, draw_rectangle, find_and_draw_rectangles, find_rectangles, get_contours


from windowcapture import WindowCapture

print("Start")


def image_preprocess(image):
    image = invert_black_white(image)
    image = opening(image, 10)
    return image


def image_to_words(image, i=None):

    image_4_rect = image_preprocess(image)
    save_image("image_4_rect", image_4_rect)
    rectangles = find_rectangles(image_4_rect, 300)

    scale_img_size = 0.005
    found_words = []

    for index, rect in enumerate(rectangles):
        cropped_image = crop_image(
            image,
            xStart=int(rect[0]*(1-scale_img_size)),
            xEnd=math.ceil((rect[0]+rect[2])*(1+scale_img_size)),
            yStart=int(rect[1]*(1-scale_img_size)),
            yEnd=math.ceil((rect[1]+rect[3])*(1+scale_img_size))
        )

        # extracting only white pixels
        number_of_white_pix = np.sum(cropped_image == 255)
        number_of_black_pix = np.sum(cropped_image == 0)

        if number_of_black_pix/(number_of_white_pix+number_of_black_pix) > 0.005:
            # if i:
            #     print(f"Image{i}")
            #     save_image(f"blue_words/ice_Image_{index}_{i}", cropped_image)
            new_word = find_text_in_image(cropped_image).replace("\n", "")
            if new_word != "":
                found_words.append(new_word)

    return found_words


def run(image, i):
    # Based on 2560, 1440
    # Character
    ignore_area_1 = [1165, 635, 230, 120]

    # Score
    ignore_area_2 = [1165, 1075, 230, 50]

    # Score line
    ignore_area_3 = [1040, 1135, 460, 5]

    # Spark
    ignore_area_4 = [968, 1309, 100, 40]

    # Fire
    ignore_area_5 = [1163, 1309, 60, 40]

    # Ice
    ignore_area_6 = [1355, 1309, 40, 40]

    # Wind
    ignore_area_7 = [1516, 1309, 80, 40]

    # Ignore middle bit
    image = draw_rectangle(image, ignore_area_1, 0)
    image = draw_rectangle(image, ignore_area_2, 0)
    image = draw_rectangle(image, ignore_area_3, 0)
    image = draw_rectangle(image, ignore_area_4, 0)
    image = draw_rectangle(image, ignore_area_5, 0)
    image = draw_rectangle(image, ignore_area_6, 0)
    image = draw_rectangle(image, ignore_area_7, 0)

    # save_image(f"image_{i%10}", image)
    start = time()

    # normal_image
    normal_image = normal_filter_mask(image)

    # ice_image
    ice_image = ice_filter_mask(image)

    normal_words = image_to_words(normal_image)
    ice_words = image_to_words(ice_image, i)

    all_words = []

    if (len(normal_words)) != 0:
        all_words.append("SPARK")
        all_words.extend(normal_words)

    if (len(ice_words)) != 0:
        all_words.append("ICE")
        all_words.extend(ice_words)

    find_time = time()

    if len(all_words) > 1:
        print(f"find text {find_time- start}")
        print(all_words)
        return all_words

    return []


wincap = WindowCapture('Epistory')
i = 0

while(True):

    if keyboard.is_pressed('esc'):
        break
    else:

        image = wincap.get_screenshot()

        # image = read_image("img1.png")

        words_to_type = run(image, i)

        if len(words_to_type) > 0:
            i = i+1
            for word_to_type in words_to_type:
                sleep(0.0001)
                keyboard.write(word_to_type)


# image = read_image("fee_issue.png")
# print(run(image, i=0))
