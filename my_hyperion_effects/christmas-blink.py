# RobC
# Simple christmas light blinker which reads n colors and blinks one color set at a time over a specified interval
import hyperion
import time
import colorsys

fps = 30
current_millis = lambda: int(round(time.time() * 1000))
off = bytearray([0, 0, 0])

def getColorArgs():
    colors = []
    for i in range(1,10):
        colorName = "color%d" % i
        colorArg = hyperion.args.get(colorName)
        if colorArg is not None:
            color = bytearray(colorArg)
            # color = colorArg
            colors.append(color)
        else:
            break
    return colors

# for i in range(1,10):
#     colorName = "color%d" % i
#     colorArg = hyperion.args.get(colorName)
#     if colorArg is not None:
#         color = bytearray(colorArg)
#         colors.append(color)
#     else:
#         break

bulbSize = hyperion.args.get('bulbSize', 2)
gapWidth = hyperion.args.get('gapWidth', 2)
interval = hyperion.args.get('changeInterval', 1)

ledData = []
colors = getColorArgs()
# init all arrays to empty
for i in range(len(colors)):
    leds = bytearray()
    ledData.append(leds)
    for i in range(hyperion.ledCount):
        leds += off

colorIndex = 0
currentColorCount = 0
currentGapCount = 0
fillingBulb = 1
for i in range(hyperion.ledCount):
    if fillingBulb:
        ledStart = i*3
        ledData[colorIndex][ledStart] = colors[colorIndex][0]
        ledData[colorIndex][ledStart+1] = colors[colorIndex][1]
        ledData[colorIndex][ledStart+2] = colors[colorIndex][2]
        currentColorCount += 1
        if currentColorCount == bulbSize:
            currentColorCount = 0
            if currentGapCount < gapWidth:
                fillingBulb = 0
            colorIndex += 1
            colorIndex = colorIndex % len(colors)
    else:
        currentGapCount += 1
        if currentGapCount == gapWidth:
            fillingBulb = 1
            currentGapCount = 0

# Start the write data loop
# switch led array every wake time to go to next color set
colorIndex = 0
while not hyperion.abort():
    hyperion.setColor(ledData[colorIndex])
    colorIndex = (colorIndex + 1) % len(ledData)
    time.sleep(interval)
