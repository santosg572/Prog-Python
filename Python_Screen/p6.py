"Grab the whole screen"
import pyscreenshot as ImageGrab

# grab fullscreen
im = ImageGrab.grab(xdisplay="")

# save image file
im.save("fullscreen.png")

