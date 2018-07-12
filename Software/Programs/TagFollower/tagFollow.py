from Rover import Rover


rover = Rover()

volt, percent = rover.getBattery()
print("Battery: {:0.4f}V ({:0.2f}%)".format(volt, percent))

# Go towards an AR tag if one is present and stop once it reaches it
rover.goToTag()

