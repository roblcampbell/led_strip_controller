from matrix_led_utils import *

# tetris pieces which fall from top to bottom and then disappear

# piece defines x,y offsets from 'base location' which are illuminated
#   base location will be the top of the piece
class MatrixTetrisPiece(FadingMatrixBulb, MatrixBulb):


    def __init__(self, color, offsets):
        FadingMatrixBulb.__init__(self, color, 0)

class MatrixScene(MatrixLedScene):
    speed = hyperion.args.get("speed")
    speedRandom = hyperion.args.get("speedRandom")
    blockCount = 1

    for i in range(blockCount):
        block = MatrixTetrisPiece([255, 0, 0])
        block.setLocation(3, 3)
        MatrixLedScene.ledObjects.append(block)

scene = MatrixScene()
scene.runScene()