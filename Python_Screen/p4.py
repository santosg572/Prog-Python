import mss
import mss.tools


with mss.mss() as sct:
    # Get information of monitor 2
    monitor_number = 0
    mon = sct.monitors[monitor_number]

    # The screen part to capture
    monitor = {
        "top": mon["top"] + 100,  # 100px from the top
        "left": mon["left"] + 100,  # 100px from the left
        "width": 600,
        "height": 500,
        "mon": monitor_number,
    }
    output = "sct-mon{mon}_{top}x{left}_{width}x{height}.png".format(**monitor)

    # Grab the data
    sct_img = sct.grab(monitor)

    # Save to the picture file
    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    print(output)


