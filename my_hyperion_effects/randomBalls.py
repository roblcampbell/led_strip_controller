<<<<<<< HEAD
import colorsys
import time
import hyperion
import random

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
    hsv = colorsys.rgb_to_hsv(color[0]/255.0, color[1]/255.0, color[2]/255.0)
    rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2]*brightness)
    adjusted = ((int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)))
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

    # 'paint' object on the led scene at the current location
    # if specified, blend this objects colors with the colors currently at the same location
    def paint(self, ledSceneArray):
        pass


class LedScene(object):
    ledObjects = []

    def runScene(self):
        print "Starting led scene loop..."
        #30 fps sleep time
        sleepTime = 1.0 / fps
        lastTime = current_millis();
        while not hyperion.abort():
            # hyperion.setColor(ledData[colorIndex])
            # colorIndex = (colorIndex + 1) % len(ledData)
            now = current_millis()
            elapsed = now - lastTime
            lastTime = now
            self.updateObjects(elapsed)

            #create a new empty scene to paint on
            ledScene = bytearray()
            for i in range(hyperion.ledCount):
                ledScene += off
            self.paintObjects(ledScene)
            hyperion.setColor(ledScene)

            time.sleep(sleepTime)

    def paintObjects(self, ledScene):
        for ledObject in self.ledObjects:
            ledObject.paint(ledScene)

    def updateObjects(self, elapsed):
        for ledObject in self.ledObjects:
            ledObject.update(elapsed)


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
            ledSceneArray[locationStart] = self.color[0]
            ledSceneArray[locationStart + 1] = self.color[1]
            ledSceneArray[locationStart + 2] = self.color[2]
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


class RandomMovingBulb(XMasBulb):
    targetDistance = 10
    startingLocation = 0

    def __init__(self, color, velocity):
        super(self.__class__, self).__init__(color)
        self.velocity = velocity

    def calcNewDistance(self):
        self.targetDistance = random.randint(0, 200)
        self.startingLocation = self.baseLocation

    def update(self, elapsedTime):
        super(RandomMovingBulb, self).update(elapsedTime)
        if self.baseLocation < 0:
            self.baseLocation = 0
            self.direction = 1
            self.calcNewDistance()
        elif self.baseLocation >= (hyperion.ledCount - self.bulbSize - 1):
            self.direction = -1
            self.calcNewDistance()
            self.baseLocation = hyperion.ledCount - self.bulbSize - 1
        elif abs(self.baseLocation - self.startingLocation) > self.targetDistance:
            self.calcNewDistance()
            self.direction = -self.direction


class RandomBallsScene(LedScene):
    colors = getColorArgs()
    fades = getFades()
    ledIndex = 0
    colorIndex = 0
    ballSize = hyperion.args.get('ballSize', 2)
    numBalls = hyperion.args.get('ballCount', 10)
    min = hyperion.args.get('minVelocity', 5.0)
    max = hyperion.args.get('maxVelocity', 10.0)

    for i in range(numBalls):
        velocity = random.uniform(min, max)
        startLoc = random.randint(10, hyperion.ledCount - 10)
        bulb = RandomMovingBulb(colors[colorIndex], velocity)
        bulb.bulbSize = ballSize
        bulb.baseLocation = startLoc
        LedScene.ledObjects.append(bulb)
        colorIndex += 1
        colorIndex = colorIndex % len(colors)

scene = RandomBallsScene()
scene.runScene()
=======
import colorsys
import time
import hyperion
import random

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
    hsv = colorsys.rgb_to_hsv(color[0]/255.0, color[1]/255.0, color[2]/255.0)
    rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2]*brightness)
    adjusted = ((int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)))
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

    # 'paint' object on the led scene at the current location
    # if specified, blend this objects colors with the colors currently at the same location
    def paint(self, ledSceneArray):
        pass


class LedScene(object):
    ledObjects = []

    def runScene(self):
        print "Starting led scene loop..."
        #30 fps sleep time
        sleepTime = 1.0 / fps
        lastTime = current_millis();
        while not hyperion.abort():
            # hyperion.setColor(ledData[colorIndex])
            # colorIndex = (colorIndex + 1) % len(ledData)
            now = current_millis()
            elapsed = now - lastTime
            lastTime = now
            self.updateObjects(elapsed)

            #create a new empty scene to paint on
            ledScene = bytearray()
            for i in range(hyperion.ledCount):
                ledScene += off
            self.paintObjects(ledScene)
            hyperion.setColor(ledScene)

            time.sleep(sleepTime)

    def paintObjects(self, ledScene):
        for ledObject in self.ledObjects:
            ledObject.paint(ledScene)

    def updateObjects(self, elapsed):
        for ledObject in self.ledObjects:
            ledObject.update(elapsed)


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
            ledSceneArray[locationStart] = self.color[0]
            ledSceneArray[locationStart + 1] = self.color[1]
            ledSceneArray[locationStart + 2] = self.color[2]
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


class RandomMovingBulb(XMasBulb):
    targetDistance = 10
    startingLocation = 0

    def __init__(self, color, velocity):
        super(self.__class__, self).__init__(color)
        self.velocity = velocity

    def calcNewDistance(self):
        self.targetDistance = random.randint(0, 200)
        self.startingLocation = self.baseLocation

    def update(self, elapsedTime):
        super(RandomMovingBulb, self).update(elapsedTime)
        if self.baseLocation < 0:
            self.baseLocation = 0
            self.direction = 1
            self.calcNewDistance()
        elif self.baseLocation >= (hyperion.ledCount - self.bulbSize - 1):
            self.direction = -1
            self.calcNewDistance()
            self.baseLocation = hyperion.ledCount - self.bulbSize - 1
        elif abs(self.baseLocation - self.startingLocation) > self.targetDistance:
            self.calcNewDistance()
            self.direction = -self.direction


class RandomBallsScene(LedScene):
    colors = getColorArgs()
    fades = getFades()
    ledIndex = 0
    colorIndex = 0
    ballSize = hyperion.args.get('ballSize', 2)
    numBalls = hyperion.args.get('ballCount', 10)
    min = hyperion.args.get('minVelocity', 5.0)
    max = hyperion.args.get('maxVelocity', 10.0)

    for i in range(numBalls):
        velocity = random.uniform(min, max)
        startLoc = random.randint(10, hyperion.ledCount - 10)
        bulb = RandomMovingBulb(colors[colorIndex], velocity)
        bulb.bulbSize = ballSize
        bulb.baseLocation = startLoc
        LedScene.ledObjects.append(bulb)
        colorIndex += 1
        colorIndex = colorIndex % len(colors)

scene = RandomBallsScene()
scene.runScene()
>>>>>>> fcb8380bca07cbd34c0c8acd8dd5abb3054bb5a3
