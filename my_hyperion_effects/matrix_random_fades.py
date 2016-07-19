from matrix_led_utils import *

# random fade-in fade-out blocks.
# when a block fades out, it picks a new available random location and moves there
# inputs : fadeCycleTimeMin
#          fadeCycleTimeMax
#          colors[1..n]
#          blockCount

class MatrixMovingRandomBlock(FadingMatrixBulb):
    def __init__(self, color, fadeCycleSeconds):
        super(self.__class__, self).__init__(color, fadeCycleSeconds)

    def maxBrightnessReached(self):
        print "max"

    def minBrightnessReached(self):
        print "min"

class MatrixScene(MatrixLedScene):
    colors = getColorArgs()
    fades = getFades()
    ledIndex = 0
    colorIndex = 0
    blockCount = 6

    for i in range(blockCount):
        cycleSeconds = fades[i % len(fades)]
        color = getRandomColor()
        # colors[i % len(colors)]
        block = MatrixMovingRandomBlock(color, cycleSeconds)
        block.fadeDirection = 1
        block.currentBrightness = random.uniform(.1, .9)
        loc = getRandomXYLocation(5, 5)
        block.setLocation(loc[0], loc[1])
        MatrixLedScene.ledObjects.append(block)

scene = MatrixScene()
scene.runScene()