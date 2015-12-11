import hyperion
import time
import colorsys

# Get the parameters
ballSpeed = float(hyperion.args.get('ball-speed', 10.0))
ballColor = hyperion.args.get('color', (255,0,0))
percentage = int(hyperion.args.get('percentage', 10))

# Check parameters
rotationTime = max(0.1, ballSpeed)
percentage = max(1, min(percentage, 100))

# Process parameters
factor = percentage/100.0
hsv = colorsys.rgb_to_hsv(ballColor[0]/255.0, ballColor[1]/255.0, ballColor[2]/255.0)

# Initialize the led data
ledData = bytearray()

#  start leds off all black
for i in range(hyperion.ledCount):
	ledData += bytearray((0, 0, 0))

# ball data
ballLocation = 0


# Calculate the sleep time and rotation increment
increment = 3
sleepTime = rotationTime / hyperion.ledCount
while sleepTime < 0.05:
	increment *= 2
	sleepTime *= 2
increment %= hyperion.ledCount

# Start the write data loop
while not hyperion.abort():
	hyperion.setColor(ledData)
	ledData = ledData[increment:] + ledData[:increment]
	time.sleep(sleepTime)
