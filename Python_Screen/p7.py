from PIL import ImageGrab

"Grab the whole screen"

# grab fullscreen
im = ImageGrab.grab(xdisplay="")

# save image file
#im.save("fullscreen.png")
im.show() 
