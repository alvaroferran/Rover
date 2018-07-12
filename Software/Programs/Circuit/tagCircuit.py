from Rover import Rover
import time


rover = Rover()

volt, percent = rover.getBattery()
print("Battery: {:0.4f}V ({:0.2f}%)".format(volt, percent))

angle = [330, 245, 330, 60]

for i in range(4):
    rover.goToTag()
    rover.setAngle(angle[i])
    time.sleep(0.1)

