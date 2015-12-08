
import RPi.GPIO as GPIO
import time
import yaml

INPUT_PIN = 18
OUTPUT_PIN = 12

GPIO.setmode(GPIO.BOARD)
# GPIO.setup(OUTPUT_PIN, GPIO.OUT)
GPIO.setup(INPUT_PIN, GPIO.IN)

try:
    # while True:
    #     GPIO.output(OUTPUT_PIN, True)
    #     time.sleep(5)
    #     GPIO.output(OUTPUT_PIN, False)
    #     time.sleep(5)

    while True:

        signal = GPIO.input(INPUT_PIN)
        print(signal)
        time.sleep(5)


except Exception:
    print("error")

finally:
    GPIO.cleanup()
