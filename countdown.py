import sys
import time

def countdown(sleeping_time):
    for remaining in range(sleeping_time, -1, -1):
        sys.stdout.write("\r")
        sys.stdout.write("Wating{:2d} seconds...".format(remaining))
        sys.stdout.flush()
        time.sleep(1)

    sys.stdout.write("\r\n\n")