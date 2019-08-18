
import cv2, time, subprocess, picamera, socket, os, signal
from multiprocessing import Process
from bs4 import BeautifulSoup
import requests
import subprocess


def createData():
    return {"authentication": "ekscn0805"}

def serverRequest(serverURL, data, upload):
    client = requests.session()
    serverURL = "http://192.168.0.68:8000/rasberrypy/" + serverURL
    html = client.get(serverURL)
    csrfToken = client.cookies["csrftoken"]
    headers = {"X-CSRFToken" : csrfToken}
    res = client.post(serverURL, files = upload,data=data,headers = headers)
    client.close()
    return res

def createBabyPicture():
    camera = picamera.PiCamera()
    imgName = time.strftime('(%m-%d %H:%M:%S)', time.localtime(time.time())) + ".jpg"
    imagePath = "./img/" + imgName
    camera.capture(imagePath)
    files = open(imagePath, "rb")
    upload = {"image": files}
    data = createData()
    return serverRequest("imageUpload", data=data, upload=upload)

def createBabyTemperature():
    proc = subprocess.Popen(["./raspberrypi_video"], stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    out = proc.communicate()[0]
    out  = float(out[:5])
    temperature = False
    if out > 37.5:
        temperature = True
    proc.stdout.close()
    data = createData()
    data["IsSick"] = temperature
    serverRequest("createBabyTemperature",data=data,upload=None)


if __name__ == "__main__":
    
    createBabyPicture()
    createBabyTemperature()

