
import RPi.GPIO as GPIO
import time
import yaml

INPUT_PIN = 18
OUTPUT_PIN = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(OUTPUT_PIN, GPIO.OUT)
# GPIO.setup(INPUT_PIN, GPIO.IN)



pattern = None
with open("ir_on.yml", "r") as f:
    pattern = yaml.load(f)

try:
    # while True:
    #     GPIO.output(OUTPUT_PIN, True)
    #     time.sleep(5)
    #     GPIO.output(OUTPUT_PIN, False)
    #     time.sleep(5)

    GPIO.output(OUTPUT_PIN, 0)


    for i in range(len(pattern[1])):
        GPIO.output(OUTPUT_PIN, 1)
        time.sleep(pattern[1][i])

        if i >= len(pattern[0]):
            GPIO.output(OUTPUT_PIN, 0)
            time.sleep(pattern[0][i])



except Exception:
    print("error")

finally:
    GPIO.cleanup()
    print("cleanup")
