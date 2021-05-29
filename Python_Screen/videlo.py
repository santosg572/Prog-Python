import cv2
import numpy as np
import pyautogui

screen_size = (1600, 900)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter("output.avi", fourcc, 10.0, (screen_size))

while True: 
   img = pyautogui.screenshot()
   frame = np.array(img)
   frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
   out.write(frame)
   cv2.imshow('hola', frame)
   if cv2.waitKey(1) == 27:
      print("END")
      break
out.release()
cv2.destroyAllWindows()
