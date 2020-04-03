import RPi.GPIO as GPIO
import time

led = 12
btn = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(led, GPIO.HIGH)
time.sleep(2)
GPIO.output(led, GPIO.LOW)
time.sleep(2)

print("Start of Program")
try:
    while True:
        if GPIO.input(btn) == GPIO.LOW:
            pwm = GPIO.PWM(led, 240)
            pwm.start(0)
            for x in range(3):
                pwm.ChangeDutyCycle(0)
                for i in range(0, 100, 5):
                    print(i)
                    time.sleep((0.05))
                    pwm.ChangeDutyCycle(i)
                pwm.ChangeDutyCycle(100)
                for i in range(100, 0, -5):
                    print(i)
                    time.sleep(0.05)
                    pwm.ChangeDutyCycle(i)    
            pwm.stop()
except KeyboardInterrupt:
    print("End of Program")
finally:
    GPIO.cleanup()
