import hyperion
import time
import colorsys

# colors = []
# while True:


# Get the parameters
color1 = bytearray(hyperion.args.get('color1', [255,0,0]))
color2 = bytearray(hyperion.args.get('color2', [0,255,0]))
color3 = bytearray(hyperion.args.get('color3', [0,0,255]))
color4 = bytearray(hyperion.args.get('color4', [255,255,0]))

colorarg4 = hyperion.args.get('color4')
if colorarg4 is not None:
    print colorarg4
else:
    print "Nunya"

# color4 = bytearray(hyperion.args.get('color4'))
# hsv1 = colorsys.rgb_to_hsv(color1[0]/255.0, color1[1]/255.0, color1[2]/255.0)
# rgb1 = colorsys.hsv_to_rgb(hsv1[0], hsv1[1], hsv1[2])
# hsv2 = colorsys.rgb_to_hsv(color2[0]/255.0, color2[1]/255.0, color2[2]/255.0)
# rgb2 = colorsys.hsv_to_rgb(hsv2[0], hsv2[1], hsv2[2])
# hsv3 = colorsys.rgb_to_hsv(color3[0]/255.0, color3[1]/255.0, color3[2]/255.0)
# rgb3 = colorsys.hsv_to_rgb(hsv3[0], hsv3[1], hsv3[2])
off = bytearray([0, 0, 0])

bulbSize = hyperion.args.get('bulbSize', 2)
gapWidth = hyperion.args.get('gapWidth', 2)
interval = hyperion.args.get('changeInterval', 1000)

colors = [color1, color2, color3, color4]

ledData1 = bytearray()
ledData2 = bytearray()
ledData3 = bytearray()
ledData4 = bytearray()
ledData = [ledData1, ledData2, ledData3, ledData4]

# init all arrays to empty
for leds in ledData:
    for i in range(hyperion.ledCount):
        leds += off

print len(ledData1)

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
            fillingBulb = 0
            colorIndex += 1
            colorIndex = colorIndex % len(colors)
    else:
        currentGapCount += 1
        if currentGapCount == gapWidth:
            fillingBulb = 1
            currentGapCount = 0

# Calculate the sleep time and rotation increment
sleepTime = 1
# Start the write data loop
colorIndex = 0
while not hyperion.abort():
    hyperion.setColor(ledData[colorIndex])
    colorIndex = (colorIndex + 1) % len(ledData)
    time.sleep(sleepTime)
