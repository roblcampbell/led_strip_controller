from ledutils import *
# take this out when moving to a new effect script #

################### matrix_led_utils import start #############################

def getAvailableRandomXYLocation(xSize, ySize, currentObjects) :
    while 1 == 1:
        loc = getRandomXYLocation(xSize, ySize)
        occupied = 0
        for obj in currentObjects:
            if obj.xLocation == loc[0] and obj.yLocation == loc[1]:
                occupied = 1
        if not occupied:
            return loc
    return [0, 0]


def getRandomXYLocation(xSize, ySize):
    return [random.randint(0, xSize - 1), random.randint(0, ySize - 1)]


# create a 2d array which maps from x,y location to linear LED #
#   the linear order starts at bottom right, and snakes back and forth to the top
#   the matrix order is defined as 0,0 being the top left, as in GUI canvas drawing
def createMappingMatrix(width, height):
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


class MatrixBulb(MatrixLedObject):
    color = [255, 0, 0]
    bulbSize = 1

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
        MatrixBulb.__init__(self, color)
        self.fadeSpeed = 1.0 / (fps * (fadeCycleSeconds / 2))
        self.baseColor = color

    def setFadeCycleSeconds(self, seconds):
        self.fadeSpeed = 1.0 / (fps * (seconds / 2))

    def update(self, elapsedTime):
        super(FadingMatrixBulb, self).update(elapsedTime)
        self.currentBrightness += (self.fadeSpeed * self.fadeDirection)
        if self.currentBrightness <= 0:
            self.currentBrightness = 0
            self.fadeDirection = -self.fadeDirection
            self.minBrightnessReached()

        if self.currentBrightness >= 1.0:
            self.currentBrightness = 1.0
            self.fadeDirection = -self.fadeDirection
            self.maxBrightnessReached()

        self.color = adjustRgbBrightness(self.baseColor, self.currentBrightness)

    def maxBrightnessReached(self):
        pass

    def minBrightnessReached(self):
        pass


class MatrixLedScene(object):
    ledObjects = []
    matrixMappings = createMappingMatrix(6, 6)

    def runScene(self):
        # 30 fps sleep time
        sleepTime = 1.0 / fps
        lastTime = current_millis();
        while not hyperion.abort():
            # hyperion.setColor(ledData[colorIndex])block = MatrixMovingRandomBlock(color, cycleSeconds)
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

# objs = []
# bulb = MatrixBulb([255, 0, 0])
# bulb.setLocation(0, 0)
# objs.append(bulb)
# bulb = MatrixBulb([255, 0, 0])
# bulb.setLocation(1, 1)
# objs.append(bulb)
# bulb = MatrixBulb([255, 0, 0])
# bulb.setLocation(2, 2)
# objs.append(bulb)
# bulb = MatrixBulb([255, 0, 0])
# bulb.setLocation(3, 3)
# objs.append(bulb)
# bulb = MatrixBulb([255, 0, 0])
# bulb.setLocation(4, 4)
# objs.append(bulb)
# bulb = MatrixBulb([255, 0, 0])
# bulb.setLocation(5, 5)
# objs.append(bulb)
#
# for i in range(100):
#     rdm = getAvailableRandomXYLocation(6, 6, objs)
#     print "%d, %d" % (rdm[0], rdm[1])

################### matrix_led_utils import end #############################
