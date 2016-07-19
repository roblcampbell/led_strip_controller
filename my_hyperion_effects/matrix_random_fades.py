from matrix_led_utils import *

# random fade-in fade-out blocks.
# when a block fades out, it picks a new available random location and moves there
# inputs : fadeCycleTimeMin
#          fadeCycleTimeMax
#          colors[1..n]
#          blockCount

class MatrixScene(MatrixLedScene):
    colors = getColorArgs()
    fades = getFades()
    ledIndex = 0
    colorIndex = 0

scene = MatrixScene()
scene.runScene()