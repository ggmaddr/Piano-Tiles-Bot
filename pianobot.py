import keyboard
import pyautogui
import numpy as np
import cv2
import time

# if you are not on windows, comment this out
import win32api, win32con


### TUNABLE PARAMETERS ###
# button to press when selecting region and quitting
start_button = "p"

# delay between taps (0 works for app but had to use 0.05 on website cuz it dies without it for some reason)
between_tap_delay = 0.00

# darkness threshold (how dark does pixel have to be to be classified as tile)
darkness_threshold = 1

# keys to use to tap tiles
keys = ['a', 's', 'd', 'f']
# keys = ['d', 'f', 'j', 'k'] # https://poki.com/en/g/piano-tiles-2

# Mouse Click or Keys
use_mouse = False

# this works faster / in more cases (only if you have windows)
use_win32 = True

# to ensure it doesn't click top of the screen and exit out by accident
# setting it to 1 works fine in most cases, but 0.8 could work better for some online games
height_multiplier = 1.0

### END TUNABLE PARAMETERS ###

# faster and more reliable than pyautogui.click()
def click(x, y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


last_lane = None
# function that finds and presses tile
def tap_tile(scrot):
    global coords, WIDTH, HEIGHT, keys, last_lane
    for ytemp in range(1, int(HEIGHT * height_multiplier), 5):
        # check each of the 4 lanes
        for i in range(4):
            if i == last_lane: continue
            last_lane = i
            x = int(i * WIDTH / 4 + WIDTH / 8)
            y = HEIGHT - ytemp
            
            if scrot[y][x] < darkness_threshold: # if dark
                if use_mouse:
                    if use_win32: # recommended over pyautogui
                        click(x + coords[0], y + coords[1])
                    else:
                        pyautogui.click(x = x + coords[0], y = y + coords[1])
                else:
                    pyautogui.write(keys[i])
                    
                # exit function if pressed a tile
                return

# position mouse to top left corner and press start_button (whatever you define) to let program record mouse location
while True:
    if keyboard.is_pressed(start_button):
        mousePos1 = pyautogui.position()
        break
    
time.sleep(1)
 
# position mouse to bottom right corner and press start_button (whatever you define) to let program record mouse location
while True:
    if keyboard.is_pressed(start_button):
        mousePos2 = pyautogui.position()
        break


# use both mouse positions to make the following variables
WIDTH = mousePos2.x - mousePos1.x
HEIGHT = mousePos2.y - mousePos1.y

time.sleep(1)

coords = (mousePos1.x, mousePos1.y, mousePos2.x, mousePos2.y)

while True:
    # pressing start_button ends the program mid-game (in case you need to quit it)
    if keyboard.is_pressed(start_button):
        break
    
    # take screenshot and pass it to the tap_tile function
    scrot = np.array(pyautogui.screenshot(region = (mousePos1.x, mousePos1.y, WIDTH, HEIGHT)))
    scrot = cv2.cvtColor(scrot, cv2.COLOR_BGR2GRAY)
    tap_tile(scrot)
    time.sleep(between_tap_delay)
    
