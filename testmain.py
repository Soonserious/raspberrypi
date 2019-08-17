import subprocess
import time
import signal
import os

proc = subprocess.Popen(["./raspberrypi_video"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
out = proc.communicate()[0]
out = float(out[:5])
print(str(out))

if out >= 37.5:
    print("1")
else:
    print("2")
