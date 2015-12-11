# collection of utility functions to handle things like color mixing, brightness fading, color
#  morphing, timed fade cycles, etc

import time
import datetime

current_millis = lambda: int(round(time.time() * 1000))

# thing which lives on a field of LEDs. It specifies a range of which led indexes it occupies,
#  so the controller can 'paint' it there and also blend it's colors with other LED objects
class LedObject(object):
    # specific location, which can be a fraction of whole led number. real paint location
    #  will be rounding of this to closest LED
    baseLocation = 0.0
    minLedIndex = 0
    maxLedIndex = 0
    # velocity value is in LEDs/sec
    velocity = 0.0
    # 0-left/1-right movement
    direction = 1

    # this is called by a controller every time a timer ticks for updating and repainting
    def update(self, elapsedTime):
        print "LEDObj update()"
        self.updateLocation(elapsedTime)

    def updateLocation(self, elapsedTime):
        if self.velocity == 0:
            return
        print "updating location"


class XMasBulb(LedObject):
    def update(self, elapsedTime):
        super(XMasBulb, self).update(elapsedTime)
        # print "Bulb.update(%d)" % elapsedTime
