import numpy as np
import pyautogui
import random
import time

current_pos = 2
last_pos = -1
match = dict(r=185, g=186, b=190)
strict_upper = 240
lower = 1302     # 530
left = 1164
middle = 1516
right = 1862
moves = ['left', 'right']
middle_upper = 240
middle_lower = 1350

start_time = time.time()

bad_color_range = [
    # Yellow
    dict(
        r=dict(low=232, high=241),
        g=dict(low=237, high=244),
        b=dict(low=165, high=175)
    ),

    # Blue
    dict(
        r=dict(low=148, high=160),
        g=dict(low=220, high=228),
        b=dict(low=226, high=238)
    ),

    # Green
    dict(
        r=dict(low=72, high=85),
        g=dict(low=212, high=220),
        b=dict(low=55, high=75)
    )
]

good_color_range = [
    # Shoes
    dict(
        name='Shoes',
        r=dict(low=20, high=35),
        g=dict(low=15, high=40),
        b=dict(low=15, high=40)
    ),

    # Chips
    dict(
        name='Chips',
        r=dict(low=220, high=240),
        g=dict(low=180, high=205),
        b=dict(low=145, high=170)
    ),

    # Guac
    dict(
        name='Guac',
        r=dict(low=100, high=125),
        g=dict(low=25, high=40),
        b=dict(low=15, high=35)
    )
]


def turn(direction):
    pyautogui.press(direction)
    return


def check_color_range(r_vals, g_vals, b_vals, color_type):
    if color_type == 'good':
        color_range = good_color_range
    else:
        color_range = bad_color_range

    for color in color_range:
        result = np.array([np.multiply((color['r']['low'] <= r_vals), (r_vals <= color['r']['high'])),
                           np.multiply((color['g']['low'] <= g_vals), (g_vals <= color['g']['high'])),
                           np.multiply((color['b']['low'] <= b_vals), (b_vals <= color['b']['high']))])
        result = np.product(result, axis=0)
        result = np.nansum(result)

        if result > 0:
            # if color_type == 'good':
            #     print(f'I found {color["name"]}!')
            return True

    return False


def check_death(rgb):
    if rgb[0] == 226 and rgb[1] == 37 and rgb[2] == 53:
        time.sleep(10)
        pyautogui.click(x=1500, y=1180)
        return True
    else:
        return False


def check_time(start):
    elapsed = time.time() - start
    if (elapsed // 60) >= 2:
        return True
    else:
        return False


while 1:

    if check_time(start_time):
        middle_lower = 950
        # print('REACHED MAX TIME LIMIT')
        # current_pos = 4

    # upper = random.randint(strict_upper, 400)
    upper = strict_upper

    if current_pos != last_pos:
        # print(f'Current Position: {current_pos}')
        last_pos = current_pos

    image = np.array(pyautogui.screenshot())
    if check_death(image[780, 1400]):
        start_time = time.time()
        middle_lower = 1350
        last_pos = -1
        current_pos = 2
        time.sleep(5)
        continue


    if current_pos == 1:
        lane = image[upper:lower, left, :]
    elif current_pos == 2:
        lane = image[upper:lower, middle, :]
    else:
        lane = image[upper:lower, right, :]

    # Extract RGB
    r = lane[:, 0]
    g = lane[:, 1]
    b = lane[:, 2]

    # Test bad color ranges
    move = check_color_range(r, g, b, 'bad')

    # Move
    if move:
        if current_pos == 1:
            turn('right')
            current_pos = 2
        elif current_pos == 2:
            rand_turn = random.randint(0, 1)
            if rand_turn:
                current_pos = 3
            else:
                current_pos = 1
            turn(moves[rand_turn])
        else:
            turn('left')
            current_pos = 2
        continue

    west = []
    east = []

    # Test good color ranges
    if current_pos == 1:
        east = image[upper:lower, middle, :]
        r = east[:, 0]
        g = east[:, 1]
        b = east[:, 2]
        if check_color_range(r, g, b, 'good'):
            turn('right')
            current_pos = 2
            continue
    elif current_pos == 2:
        west = image[upper:lower, left, :]
        r = west[:, 0]
        g = west[:, 1]
        b = west[:, 2]
        if check_color_range(r, g, b, 'good'):
            turn('left')
            current_pos = 1
            continue
        else:
            east = image[upper:lower, right, :]
            r = east[:, 0]
            g = east[:, 1]
            b = east[:, 2]
            if check_color_range(r, g, b, 'good'):
                turn('right')
                current_pos = 3
                continue

    else:
        west = image[upper:lower, middle, :]
        r = west[:, 0]
        g = west[:, 1]
        b = west[:, 2]
        if check_color_range(r, g, b, 'good'):
            turn('left')
            current_pos = 2
            continue

    # lane = image[middle_upper:middle_lower, middle, :]
    # r = lane[:, 0]
    # g = lane[:, 1]
    # b = lane[:, 2]
    # if not check_color_range(r, g, b, 'bad'):
    #     if current_pos == 1:
    #         lane = image[upper:lower, left, :]
    #         r = lane[:, 0]
    #         g = lane[:, 1]
    #         b = lane[:, 2]
    #         if not check_color_range(r, g, b, 'good'):
    #             turn('right')
    #             current_pos = 2
    #     if current_pos == 3:
    #         lane = image[upper:lower, right, :]
    #         r = lane[:, 0]
    #         g = lane[:, 1]
    #         b = lane[:, 2]
    #         if not check_color_range(r, g, b, 'good'):
    #             turn('left')
    #             current_pos = 2
