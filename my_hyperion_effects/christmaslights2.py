# RobC
# Simple christmas light blinker which reads n colors and blinks one color set at a time over a specified interval
from ledutils import *
import random

class ChristmasLightsScene(LedScene):
    colors = getColorArgs()
    fades = getFades(len(colors))
    ledIndex = 0
    colorIndex = 0
    bulbSize = hyperion.args.get('bulbSize', 2)
    gapWidth = hyperion.args.get('gapWidth', 1)
    # fades = [random.uniform(3.0, 3.5), random.uniform(3.7, 4.2), random.uniform(4.4, 4.9), random.uniform(5.1, 5.6)]
    while True:
        color = colors[colorIndex]
        fadeSeconds = fades[colorIndex]
        bulb = FadingXmasBulb(color, fadeSeconds)

    # bulb1 = FadingXmasBulb([255, 0, 0], 5)
        bulb.baseLocation = ledIndex
        LedScene.ledObjects.append(bulb)

        colorIndex = (colorIndex+1) % len(colors)
        ledIndex += (bulbSize + gapWidth)
    # bulb1.velocity = 5
    # bulb1.direction = -bulb1.direction
        if (ledIndex >= hyperion.ledCount - 1):
            break

xmasScene = ChristmasLightsScene()
xmasScene.runScene()
