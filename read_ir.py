
import RPi.GPIO as GPIO
import time

INPUT_PIN = 4
OUTPUT_PIN = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(OUTPUT_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(OUTPUT_PIN, True)
        time.sleep(5)
        GPIO.output(OUTPUT_PIN, False)
        time.sleep(5)

except Exception:
    print("error")

finally:
    GPIO.cleanup()
