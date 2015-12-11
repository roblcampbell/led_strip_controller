import time
import colorsys

class Snake:
    ledLength = 0
    rotationTime = 10.0
    color = [255, 0, 0]
    percentage = 25
    snakeLeds = 0
    # the array of the leds for the scene, with black for all leds but the snake itself
    ledData = bytearray()

    def __init__(self, ledLength, rotationTime, color, percentage):
        self.ledLength = ledLength
        self.rotationTime = rotationTime
        self.color = color
        self.percentage = percentage

        # calculate LED length and array, etc
        self.refresh()

    def refresh(self):
        # Check parameters
        self.rotationTime = max(0.1, self.rotationTime)
        self.percentage = max(1, min(self.percentage, 100))

        # Process parameters
        hsv = colorsys.rgb_to_hsv(self.color[0]/255.0, self.color[1]/255.0, self.color[2]/255.0)

        # Initialize the led data
        self.snakeLeds = max(1, int(self.ledLength*(self.percentage/100.0)))
        for i in range(1,self.snakeLeds+1):
            rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1],
                                      hsv[2]*(self.snakeLeds-i)/self.snakeLeds)
            self.ledData += bytearray((int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)))

    # called every time the animation timer ticks
    def update(self):
        # find time difference

        # determine change in color, brightness, location, etc

        # change led array properties accordingly
        pass

