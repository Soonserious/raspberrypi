import cv2
import sys
import subprocess

img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
#cv2.imshow('image', img)
#cv2.destroyAllWindows()
sys.stdout.write('1')
