
import RPi.GPIO as GPIO
import time
import yaml

INPUT_PIN = 18
OUTPUT_PIN = 12

GPIO.setmode(GPIO.BOARD)
# GPIO.setup(OUTPUT_PIN, GPIO.OUT)
GPIO.setup(INPUT_PIN, GPIO.IN)


pattern = []


try:
    # while True:
    #     GPIO.output(OUTPUT_PIN, True)
    #     time.sleep(5)
    #     GPIO.output(OUTPUT_PIN, False)
    #     time.sleep(5)

    t_start = None
    past_signal = 0


    while True:

        signal = 1 - GPIO.input(INPUT_PIN)

        if past_signal != signal:
            if t_start:
                t_end = time.time()
                t = t_end - t_start
                pattern.append(t)
                t_start = t_end
            else:
                t_start = time.time()

            past_signal = signal

        time.sleep(0.000001)







except Exception:
    print("error")

finally:
    GPIO.cleanup()
    print("cleanup")

    print(pattern)
    print(len(pattern))

    with open("ir_on.yml", "w") as f:
        yaml.dump(pattern, f)

    print("saved")
