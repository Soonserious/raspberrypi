import cv2, time, subprocess, picamera, socket, os, signal
from multiprocessing import Process
from bs4 import BeautifulSoup
import requests


if __name__ == "__main__":
    camera = picamera.Camera()
    imgName = time.strftime('(%m-%d %H:%M:%S)', time.localtime(time.time()))+".jpg"
    imagePath = "./img/"+ imgName
    camera.capture(imagePath)
    html = requests.get("192.168.0.68/rasberrypy/imageUpload")
    soup = BeautifulSoup(html,"html.parser")
    csrfToken = soup.select("body > form > input[type=hidden]:nth-child(1)")
    files = open(imagePath,"rb")
    upload = {"image" : files}
    data = {"authentication" : "ekscn0805"}
    res = requests.post("192.168.0.68/rasberrypy/imageUpload",upload=files,data=data)

