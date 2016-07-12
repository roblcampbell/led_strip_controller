# collection of utility functions to handle things like color mixing, brightness fading, color
#  morphing, timed fade cycles, etc
import hyperion
import time
import colorsys
import random

fps = 30
current_millis = lambda: int(round(time.time() * 1000))
off = bytearray([0, 0, 0])

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


# thing which lives on a matrix of LEDs. has a location
class MatrixLedObject(object):
    # specific location, which can be a fraction of whole led number. real paint location
    #  will be rounding of this to closest LED
    xLocation = 0
    yLocation = 0
    # velocity value is in LEDs/sec
    velocityX = 0.0
    velocityY = 0.0
    # 0-left/1-right movement
    directionX = 1
    directionY = 1

    def setLocation(self, x, y):
        self.xLocation = x
        self.yLocation = y

    # this is called by a controller every time a timer ticks for updating and repainting
    def update(self, elapsedTime):
        # print "LEDObj update()"
        self.updateLocation(elapsedTime)

    def updateLocation(self, elapsedTime):
        # print "update location with vel = %f" % self.velocity
        if self.velocityX == 0 and self.velocityY == 0:
            return

        distanceX = (elapsedTime / 1000.0) * self.velocityX * self.directionX
        self.xLocation += distanceX
        distanceY = (elapsedTime / 1000.0) * self.velocityY * self.directionY
        self.yLocation += distanceY
        if self.xLocation >= 6:
            self.xLocation = 0
        elif self.xLocation < 0:
            self.xLocation = 5
        if self.yLocation >= 6:
            self.yLocation = 0
        elif self.yLocation < 0:
            self.yLocation = 5

    # 'paint' object on the led scene at the current location
    # if specified, blend this objects colors with the colors currently at the same location
    def paint(self, ledSceneArray, matrixMappings):
        pass

    def setLedColor(self, ledArray, matrixMappings, x, y, color):
        ledArrayStart = matrixMappings[int(x)][int(y)] * 3
        if ledArrayStart >= len(ledArray):
            return
        ledArray[ledArrayStart] = color[0]
        ledArray[ledArrayStart + 1] = color[1]
        ledArray[ledArrayStart + 2] = color[2]

# create a 2d array which maps from x,y location to linear LED #
#   the linear order starts at bottom right, and snakes back and forth to the top
#   the matrix order is defined as 0,0 being the top left, as in GUI canvas drawing
def createMappingMatrix(width, height) :
    ledX = width - 1
    ledY = height - 1

    matrix = [[0]*6 for i in range(6)]

    direction = -1
    ledNumber = 0
    while ledY >= 0:
        matrix[ledX][ledY] = ledNumber
        ledNumber = ledNumber + 1
        ledX += direction
        if ledX < 0:
            ledX = 0
            direction = -direction
            ledY = ledY - 1
        elif ledX >= width:
            ledX = width - 1
            direction = -direction
            ledY = ledY - 1
    return matrix


class MatrixBulb(MatrixLedObject):
    color = [255, 0, 0]
    bulbSize = 2

    def __init__(self, color):
        self.color = color

    def update(self, elapsedTime):
        super(MatrixBulb, self).update(elapsedTime)
        # print "Bulb.update(%d)" % elapsedTime

    def paint(self, ledSceneArray, matrixMappings):
        # print "Bulb.paint"
        # print "location %d" % locationStart
        # print "led scene size %d" % len(ledSceneArray)
        for i in range(self.bulbSize):
            # ledSceneArray[locationStart] = self.color[0]
            # ledSceneArray[locationStart + 1] = self.color[1]
            # ledSceneArray[locationStart + 2] = self.color[2]
            super(MatrixBulb, self).setLedColor(ledSceneArray,  matrixMappings, self.xLocation, self.yLocation, self.color)

class FadingMatrixBulb(MatrixBulb):
    baseColor = [0, 0, 0]
    fadeSpeed = 0.0
    currentBrightness = 1.0
    fadeDirection = -1

    def __init__(self, color, fadeCycleSeconds):
        super(self.__class__, self).__init__(color)
        self.fadeSpeed = 1.0 / (fps * (fadeCycleSeconds / 2))
        self.baseColor = color

    def update(self, elapsedTime):
        super(FadingMatrixBulb, self).update(elapsedTime)
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
    matrixMappings = createMappingMatrix(6, 6)

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
            self.paintObjects(ledScene, self.matrixMappings)

            # tmpLeds = new bytearray((255, 0, 0))
            # hyperion.setColor(tmpLeds)
            hyperion.setColor(ledScene)
            time.sleep(sleepTime)

    def paintObjects(self, ledScene, matrixMappings):
        for ledObject in self.ledObjects:
            ledObject.paint(ledScene, matrixMappings)

    def updateObjects(self, elapsed):
        for ledObject in self.ledObjects:
            ledObject.update(elapsed)

# ------------------END OF LED_UTILS MANUAL IMPORT--------------------------

class MatrixTesterScene(LedScene):
    colors = getColorArgs()
    fades = getFades()
    ledIndex = 0
    colorIndex = 0

    bulb = MatrixBulb([255, 0, 0])
    bulb.bulbSize = 1
    bulb.setLocation(0, 0)
    bulb.velocityX = -2
    bulb.velocityY = 1.3
    LedScene.ledObjects.append(bulb)

    bulb = MatrixBulb([0, 255, 0])
    bulb.bulbSize = 1
    bulb.setLocation(0, 5)
    bulb.velocityX = 3
    bulb.velocityY = 0.5

    LedScene.ledObjects.append(bulb)

    bulb = MatrixBulb([0, 0, 255])
    bulb.bulbSize = 1
    bulb.setLocation(5, 5)
    bulb.velocityX = 3
    bulb.velocityY = -2

    LedScene.ledObjects.append(bulb)

    bulb = MatrixBulb([255, 255, 0])
    bulb.bulbSize = 1
    bulb.setLocation(5, 0)
    bulb.velocityX = 3
    bulb.velocityY = 2
    LedScene.ledObjects.append(bulb)

scene = MatrixTesterScene()
scene.runScene()
