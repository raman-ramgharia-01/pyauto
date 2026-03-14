import pyautogui
import time
pyautogui.moveTo( 79, 744, duration=1)

pyautogui.click()

pyautogui.typewrite('edge')

pyautogui.press('enter')

time.sleep(4)

pyautogui.typewrite('https://legend-raman.netlify.app/')
pyautogui.press('enter')

time.sleep(2)

pyautogui.keyDown('alt')
pyautogui.press('tab')

# most importent
pyautogui.keyUp('alt')


