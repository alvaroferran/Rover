from Rover import Rover


rover = Rover()

volt, percent = rover.getBattery()
print("Battery: {:0.4f}V ({:0.2f}%)".format(volt, percent))

angle = 90

# Turn angle degrees relative to the rover's current orientation
rover.turnDegrees(angle)

# Go to angle degrees relative to the Earth's magnetic pole
# rover.setAngle(angle)

