import hyperion
import time
import colorsys
import random

fps = 30
current_millis = lambda: int(round(time.time() * 1000))
off = bytearray([0, 0, 0])


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


def getFadeSpeed():
    fadeSpeedArg = hyperion.args.get("fadeSpeed1")
    if fadeSpeedArg is not None:
        return fadeSpeedArg
    else:
        return 1.0


def adjustRgbBrightness(color, brightness):
    hsv = colorsys.rgb_to_hsv(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)
    rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2] * brightness)
    adjusted = ((int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)))
    return adjusted


# thing which lives on a field of LEDs. It specifies a range of which led indexes it occupies,
#  so the controller can 'paint' it there and also blend it's colors with other LED objects
class LedObject(object):
    # specific location, which can be a fraction of whole led number. real paint location
    #  will be rounding of this to closest LED
    baseLocation = 0.0
    # velocity value is in LEDs/sec
    velocity = 0.0
    # 0-left/1-right movement
    direction = 1

    def setLocation(self, location):
        self.baseLocation = location

    # this is called by a controller every time a timer ticks for updating and repainting
    def update(self, elapsedTime):
        # print "LEDObj update()"
        self.updateLocation(elapsedTime)

    def updateLocation(self, elapsedTime):
        # print "update location with vel = %f" % self.velocity
        if self.velocity == 0:
            return
        # print "updating location"

        distance = (elapsedTime / 1000.0) * self.velocity * self.direction
        self.baseLocation += distance
        if self.baseLocation >= hyperion.ledCount - 1:
            self.baseLocation = 0
        elif self.baseLocation < 0:
            self.baseLocation = hyperion.ledCount - 1

    # 'paint' object on the led scene at the current location
    # if specified, blend this objects colors with the colors currently at the same location
    def paint(self, ledSceneArray):
        pass

    def setLedColor(self, ledArray, ledArrayStart, color):
        if ledArrayStart >= len(ledArray):
            return
        ledArray[ledArrayStart] = color[0]
        ledArray[ledArrayStart + 1] = color[1]
        ledArray[ledArrayStart + 2] = color[2]


class ColorBlob(LedObject):
    color = [255, 0, 0]
    blobSize = 2

    def __init__(self, color):
        self.color = color

    def update(self, elapsedTime):
        super(ColorBlob, self).update(elapsedTime)
        # print "Bulb.update(%d)" % elapsedTime

    def paint(self, ledSceneArray):
        # print "Bulb.paint"
        locationStart = int(self.baseLocation) * 3
        # print "location %d" % locationStart
        # print "led scene size %d" % len(ledSceneArray)
        for i in range(self.blobSize):
            # ledSceneArray[locationStart] = self.color[0]
            # ledSceneArray[locationStart + 1] = self.color[1]
            # ledSceneArray[locationStart + 2] = self.color[2]
            super(ColorBlob, self).setLedColor(ledSceneArray, locationStart, self.color)
            locationStart += 3


class FadingColorBlob(ColorBlob):
    baseColor = [0, 0, 0]
    fadeSpeed = 0.0
    currentBrightness = 1.0
    fadeDirection = -1

    def __init__(self, color, fadeCycleSeconds):
        super(self.__class__, self).__init__(color)
        self.fadeSpeed = 1.0 / (fps * (fadeCycleSeconds / 2))
        self.baseColor = color

    def update(self, elapsedTime):
        super(FadingColorBlob, self).update(elapsedTime)
        self.currentBrightness += (self.fadeSpeed * self.fadeDirection)
        if self.currentBrightness <= 0:
            self.currentBrightness = 0
            self.fadeDirection = -self.fadeDirection

        if self.currentBrightness >= 1.0:
            self.currentBrightness = 1.0
            self.fadeDirection = -self.fadeDirection

        self.color = adjustRgbBrightness(self.baseColor, self.currentBrightness)


class LedScene(object):
    ledObjects = []

    def runScene(self):
        # 30 fps sleep time
        sleepTime = 1.0 / fps
        lastTime = current_millis();
        while not hyperion.abort():
            # hyperion.setColor(ledData[colorIndex])
            # colorIndex = (colorIndex + 1) % len(ledData)
            now = current_millis()
            elapsed = now - lastTime
            lastTime = now
            self.updateObjects(elapsed)

            # create a new empty scene to paint on
            ledScene = bytearray()
            for i in range(hyperion.ledCount):
                ledScene += off
            self.paintObjects(ledScene)

            # tmpLeds = new bytearray((255, 0, 0))
            # hyperion.setColor(tmpLeds)
            hyperion.setColor(ledScene)
            time.sleep(sleepTime)

    def paintObjects(self, ledScene):
        for ledObject in self.ledObjects:
            ledObject.paint(ledScene)

    def updateObjects(self, elapsed):
        for ledObject in self.ledObjects:
            ledObject.update(elapsed)
        self.updateComplete()

    def updateComplete(self):
        pass

class BouncyBallScene(LedScene):
    colors = getColorArgs()
    fades = getFades()
    ledIndex = 0
    colorIndex = 0
    ballSize = hyperion.args.get('bouncyBallSize', 2)
    startVelocity = hyperion.args.get('bouncyBallVelocity', 50)
    blockSizeLeft = hyperion.args.get('bouncyBallBlockSizeLeft', 5)
    blockSizeRight = hyperion.args.get('bouncyBallBlockSizeRight', 5)
    velocityIncrement = hyperion.args.get('bouncyBallVelocityIncrement', 0)

    leftBlocks = []
    rightBlocks = []

    ball = ColorBlob(colors[0])
    ball.baseLocation = blockSizeLeft + 100
    ball.blobSize = ballSize
    ball.velocity = startVelocity
    LedScene.ledObjects.append(ball)

    def getLeftBound(self):
        if not self.leftBlocks:
            return 1
        leftBlock = self.leftBlocks[-1]
        return leftBlock.baseLocation + leftBlock.blobSize + 1

    def getRightBound(self):
        if not self.rightBlocks:
            return hyperion.ledCount - 2
        rightBlock = self.rightBlocks[-1]
        return rightBlock.baseLocation

    def updateComplete(self):
        if self.ball.baseLocation + self.ballSize > self.getRightBound():
            self.collision(False)
        elif self.ball.baseLocation < self.getLeftBound():
            self.collision(True)

    def collision(self, leftSide):
        if self.getRightBound() - self.getLeftBound() < self.blockSizeLeft + self.blockSizeRight + self.ballSize + 1:
            self.doCompletion()
            return

        self.ball.direction = -self.ball.direction
        self.ball.velocity += self.velocityIncrement

        if leftSide:
            block = ColorBlob(self.colors[2])
            LedScene.ledObjects.append(block)
            block.blobSize = self.blockSizeRight
            block.baseLocation = self.rightBlocks[-1].baseLocation - self.blockSizeRight
            self.rightBlocks.append(block)
            self.ball.baseLocation = self.getLeftBound()
        else:
            block = ColorBlob(self.colors[1])
            LedScene.ledObjects.append(block)
            block.blobSize = self.blockSizeLeft
            block.baseLocation = self.leftBlocks[-1].baseLocation + self.blockSizeLeft
            self.leftBlocks.append(block)
            self.ball.baseLocation = self.getRightBound() - self.blockSizeLeft

    def doCompletion(self):
        LedScene.ledObjects = []
        lBlock = ColorBlob(self.colors[1])
        lBlock.baseLocation = 0
        lBlock.blobSize = self.blockSizeLeft
        LedScene.ledObjects.append(lBlock)
        self.leftBlocks.append(lBlock)

        rBlock = ColorBlob(self.colors[2])
        rBlock.baseLocation = hyperion.ledCount - self.blockSizeRight
        rBlock.blobSize = self.blockSizeRight
        LedScene.ledObjects.append(rBlock)
        self.rightBlocks.append(rBlock)

        self.ball.velocity = self.startVelocity
        LedScene.ledObjects.append(self.ball)

        self.leftBlocks = [lBlock]
        self.rightBlocks = [rBlock]


ballScene = BouncyBallScene()
ballScene.doCompletion()
ballScene.runScene()
