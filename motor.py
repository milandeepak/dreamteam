import RPi.GPIO as GPIO          
from time import sleep

in3 = 23
in4 = 24
en = 25
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p=GPIO.PWM(en,1000)
p.start(25)

print("The default speed & direction of motor is LOW & Forward.....")

# Run the motor
print("run")
if(temp1==1):
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    print("forward")
else:
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    print("backward")

# Set the speed to low
print("low")
p.ChangeDutyCycle(75)

# If you want to stop the motor after some time, use the sleep function and then cleanup
sleep(10)  # Run the motor for 10 seconds
GPIO.cleanup()