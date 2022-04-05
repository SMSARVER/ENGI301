from bbpystepper import Stepper
mystepper = Stepper()
mystepper.rotate(180, 10) # Rotates motor 180 degrees at 10 RPM
mystepper.rotate(-180, 5) # Rotates motor back 180 degrees at 5 RPM
mystepper.angle