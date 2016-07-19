from matrix_led_utils import *

class MatrixTesterScene(MatrixLedScene):
    colors = getColorArgs()
    fades = getFades()
    ledIndex = 0
    colorIndex = 0

    bulb = MatrixBulb([255, 0, 0])
    bulb.bulbSize = 1
    bulb.setLocation(0, 0)
    bulb.velocityX = -2
    bulb.velocityY = 1.3
    MatrixLedScene.ledObjects.append(bulb)

    bulb = MatrixBulb([0, 255, 0])
    bulb.bulbSize = 1
    bulb.setLocation(0, 5)
    bulb.velocityX = 3
    bulb.velocityY = 0.5

    MatrixLedScene.ledObjects.append(bulb)

    bulb = MatrixBulb([0, 0, 255])
    bulb.bulbSize = 1
    bulb.setLocation(5, 5)
    bulb.velocityX = 3
    bulb.velocityY = -2

    MatrixLedScene.ledObjects.append(bulb)

    bulb = MatrixBulb([255, 255, 0])
    bulb.bulbSize = 1
    bulb.setLocation(5, 0)
    bulb.velocityX = 3
    bulb.velocityY = 2
    MatrixLedScene.ledObjects.append(bulb)

scene = MatrixTesterScene()
scene.runScene()
