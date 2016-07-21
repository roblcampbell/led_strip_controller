from matrix_led_utils import *

# random fade-in fade-out blocks.
# when a block fades out, it picks a new available random location and moves there
# inputs : fadeCycleTimeMin
#          fadeCycleTimeMax
#          colors[1..n]
#          blockCount

class MatrixMovingRandomBlock(FadingMatrixBulb, MatrixBulb):
    allObjects = []

    def __init__(self, color, fadeCycleSeconds, objs):
        FadingMatrixBulb.__init__(self, color, fadeCycleSeconds)
        self.allObjects = objs

    def minBrightnessReached(self):
        loc = getAvailableRandomXYLocation(6, 6, self.allObjects)
        self.setLocation(loc[0], loc[1])
        randomArg = hyperion.args.get("randomColor")
        if randomArg is not None:
            self.baseColor = getRandomColor()
        self.setFadeCycleSeconds(random.uniform(fadeBase - fadeRandom, fadeBase + fadeRandom))


class MatrixScene(MatrixLedScene):
    colors = getColorArgs()
    fades = getFades()
    ledIndex = 0
    colorIndex = 0
    blockCount = hyperion.args.get("blockCount")

    for i in range(blockCount):
        cycleSeconds = random.uniform(fadeBase - fadeRandom, fadeBase + fadeRandom)
        color = colors[i % len(colors)]
        block = MatrixMovingRandomBlock(color, cycleSeconds, MatrixLedScene.ledObjects)
        block.fadeDirection = 1
        block.currentBrightness = random.uniform(.1, .9)
        loc = getRandomXYLocation(5, 5)
        block.setLocation(loc[0], loc[1])
        MatrixLedScene.ledObjects.append(block)

scene = MatrixScene()
scene.runScene()