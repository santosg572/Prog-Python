import cv2
import numpy as np
import pyautogui

screen_size = (1600, 900)
fourcc = cv2.VideoWriter_fourcc(*"XVID")

img = pyautogui.screenshot()
frame = np.array(img)
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
cv2.imshow('polo', frame)
cv2.waitKey(0)

cv2.imwrite('messigray.png', frame)
