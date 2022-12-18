import pytesseract
import pyautogui
import cv2
import numpy as np
import logging
import colorlog

class PrependFilter(logging.Filter):
    def filter(self, record):
        record.msg = "[TFT ROLLDOWN V0.1] - " + record.msg
        return True

# Set up a logging formatter with the desired formatting
formatter = logging.Formatter('\033[33m[GOLD LEFT: %(message)s]\033[0m - Text detected at %(x)s,%(y)s: \033[32m%(champion_text)s\033[0m')

# Set up a logger and set the formatter for the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Set up a handler and set the formatter for the handler
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

words_to_detect = ['Lulu', 'Galio', 'Nasus', 'Gangplank', 'Lee Sin', 'Malphite']
champion_coordinates = [(649, 1388), (912, 1388), (1183, 1388), (1453, 1388), (1720, 1388)]
gold_x = 1162
gold_y = 1178

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
champion_config = ('-l eng --oem 1 --psm 3')
gold_config = ('-l eng --oem 1 --psm 6')

champion_width = 200
gold_width = 60
gold_height = 33

x_min = min(x for x, y in champion_coordinates)
y_min = min(y for x, y in champion_coordinates)
x_max = max(x for x, y in champion_coordinates)
y_max = max(y for x, y in champion_coordinates)

all_champion_width = x_max - x_min + champion_width
all_champion_height = 33

while True:    
    champion_screenshot = pyautogui.screenshot(region=(x_min, y_min, all_champion_width, all_champion_height))
    champion_screenshot = np.array(champion_screenshot)    
    gold_screenshot = pyautogui.screenshot(region=(gold_x, gold_y, gold_width, gold_height))    
    gold_screenshot = np.array(gold_screenshot)
    gold_text = pytesseract.image_to_string(gold_screenshot, config=gold_config).strip()   
    if str(gold_text) == "" or not gold_text.isnumeric():
        print("<Uh oh, I can't see any gold (Make sure you are playing in Fullscreen)>")
    elif int(gold_text) <= 3:
        print("<Nice rolldown! Time to econ back up>")
        break
    else:
        for x, y in champion_coordinates:
            champion_img = champion_screenshot[y-y_min:y-y_min+100, x-x_min:x-x_min+champion_width]
            champion_img = cv2.cvtColor(champion_img, cv2.COLOR_BGR2GRAY)
            champion_text = pytesseract.image_to_string(champion_img, config=champion_config)
            cv2.imwrite('champion.png', champion_img)
            logger.info(gold_text.strip(), extra={'x': str(x), 'y': str(y), 'champion_text': champion_text.strip()})
            for word in words_to_detect:
                if word in champion_text:
                    print("<Bought " + champion_text + ">")
                    #pyautogui.mouseDown(x, y, button='left')
                    #pyautogui.mouseUp(x, y, button='left')
                    break
        print("<Refreshing shop...>")
        #pyautogui.mouseDown(562, 1377, button='left')
        #pyautogui.mouseUp(562, 1377, button='left')