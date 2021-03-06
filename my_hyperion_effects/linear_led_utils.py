# This includes a dup of all the matrix/linear agnostic functions. Making a change to these
#  pieces should be reflected in both linear and matrix led utils files.
from ledutils import *
####################### Linear LED Utils import start #############################

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
        if self.baseLocation >= hyperion.ledCount:
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


class XMasBulb(LedObject):
    color = [255, 0, 0]
    bulbSize = 2

    def __init__(self, color):
        self.color = color

    def update(self, elapsedTime):
        super(XMasBulb, self).update(elapsedTime)
        # print "Bulb.update(%d)" % elapsedTime

    def paint(self, ledSceneArray):
        # print "Bulb.paint"
        locationStart = int(self.baseLocation) * 3
        # print "location %d" % locationStart
        # print "led scene size %d" % len(ledSceneArray)
        for i in range(self.bulbSize):
            # ledSceneArray[locationStart] = self.color[0]
            # ledSceneArray[locationStart + 1] = self.color[1]
            # ledSceneArray[locationStart + 2] = self.color[2]
            super(XMasBulb, self).setLedColor(ledSceneArray, locationStart, self.color)
            locationStart += 3


class FadingXmasBulb(XMasBulb):
    baseColor = [0, 0, 0]
    fadeSpeed = 0.0
    currentBrightness = 1.0
    fadeDirection = -1

    def __init__(self, color, fadeCycleSeconds):
        super(self.__class__, self).__init__(color)
        self.fadeSpeed = 1.0 / (fps * (fadeCycleSeconds / 2))
        self.baseColor = color

    def update(self, elapsedTime):
        super(FadingXmasBulb, self).update(elapsedTime)
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

################### End of linear_led_utils import ##########################