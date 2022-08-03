import pyautogui
import time 


i = 1 
while i <=5 :
      pyautogui.screenshot(str(i)+".png")
      i += 1
      time.sleep(3)