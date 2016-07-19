# collection of utility functions to handle things like color mixing, brightness fading, color
#  morphing, timed fade cycles, etc
import hyperion
import time
import colorsys
import random

fps = 30
current_millis = lambda: int(round(time.time() * 1000))
off = bytearray([0, 0, 0])

def getRandomColor():
    return [random.randint(0, 255), random.randint(0, 255),random.randint(0, 255)]

def getNumberedArgs(prefix):
    args = []
    for i in range(1, 10):
        name = "%s%d" % (prefix, i)
        arg = hyperion.args.get(name)
        if arg is not None:
            args.append(arg)
        else:
            break
    return args

# in the config, it will read all values like color1, color2, color3 and
#   return an array of the colors
def getColorArgs():
    colors = []
    for i in range(1, 10):
        colorName = "color%d" % i
        colorArg = hyperion.args.get(colorName)
        if colorArg is not None:
            color = bytearray(colorArg)
            # color = colorArg
            colors.append(color)
        else:
            break
    return colors

# reads N number of fades, and must match the length of color args
def getFades():
    fades = []
    fadeRandom = hyperion.args.get("fadeRandom")
    for i in range(1, 10):
        fadeName = "fadeSpeed%d" % i
        fadeArg = hyperion.args.get(fadeName)
        if fadeArg is not None:
            fade = random.uniform(fadeArg - fadeRandom, fadeArg + fadeRandom)
            fades.append(fade)
    return fades

def adjustRgbBrightness(color, brightness):
    hsv = colorsys.rgb_to_hsv(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
    rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2] * brightness)
    adjusted = ((int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)))
    return adjusted


# ------------------END OF LED_UTILS MANUAL IMPORT--------------------------
