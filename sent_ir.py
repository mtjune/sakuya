
import RPi.GPIO as GPIO
import time
import yaml
import math

INPUT_PIN = 18
OUTPUT_PIN = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(OUTPUT_PIN, GPIO.OUT)
# GPIO.setup(INPUT_PIN, GPIO.IN)



pattern = None
with open("ir_on.yml", "r") as f:
    pattern = yaml.load(f)


pattern_conform = {1:[], 0:[]}

t_start = None
past_signal = 0

try:
    # while True:
    #     GPIO.output(OUTPUT_PIN, True)
    #     time.sleep(5)
    #     GPIO.output(OUTPUT_PIN, False)
    #     time.sleep(5)

    GPIO.output(OUTPUT_PIN, 1)



    t_start = time.time()
    for i in range(len(pattern[1])):
        GPIO.output(OUTPUT_PIN, 0)
        # time.sleep(pattern[1][i])
        while True:
            if pattern[1][i] =< time.time() - t_start:
                break
        t_end = time.time()
        pattern_conform[1].append(t_end - t_start)
        t_start = t_end

        if i < len(pattern[0]):
            GPIO.output(OUTPUT_PIN, 1)
            # time.sleep(pattern[0][i])
            while True:
                if pattern[0][i] =< time.time() - t_start:
                    break
            pattern_conform[0].append(t_end - t_start)
            t_start = t_end



except Exception as e:
    print("error")
    print(e)

finally:
    GPIO.cleanup()
    print("cleanup")


pattern_error = {1:[], 0:[]}

error_max1 = 0.
error_max0 = 0.

for i in range(len(pattern[1])):
    tmp = abs(pattern_conform[1][i] - pattern[1][i])
    pattern_error[1].append(tmp)
    if tmp > error_max1:
        error_max1 = tmp

for i in range(len(pattern[0])):
    tmp = abs(pattern_conform[0][i] - pattern[0][i])
    pattern_error[0].append(tmp)
    if tmp > error_max0:
        error_max0 = tmp

print("1", error_max1)
print("0", error_max0)



with open("ir_error.yml", "w") as f:
    yaml.dump(pattern_error, f)
print("saved")
