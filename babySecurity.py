import cv2, time, subprocess, picamera, socket, os, signal
from multiprocessing import Process
from bs4 import BeautifulSoup
import requests
import subprocess
import argparse
import secrets
import logging


logging.basicConfig(filename="./status.log",level=logging.DEBUG)

def createData():
    return {"authentication": "ekscn0805"}


def serverRequest(serverURL, data, upload):
    client = requests.session()
    serverURL = "http://192.168.0.68:8000/rasberrypy/" + serverURL
    csrfToken = client.cookies["csrftoken"]
    headers = {"X-CSRFToken": csrfToken}
    res = client.post(serverURL, files=upload, data=data, headers=headers).json()
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
    proc = subprocess.Popen(["./raspberrypi_video"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out = proc.communicate()[0]
    out = float(out[:5])
    temperature = False
    if out > 37.5:
        temperature = True
    proc.stdout.close()
    data = createData()
    data["IsSick"] = temperature
    serverRequest("createBabyTemperature", data=data, upload=None)

def createKey():
    key = secrets.token_hex(16)
    data = {"authentication" : key}
    result = serverRequest("createProduction", data= data,upload=None)
    if result["status"]:
        logging.debug("not Authentication")
    else:
        with open("/authentication.txt","w") as f:
            f.write(result["authentication"])
            f.close()
        os.chmod("/authentication.txt",744)

def createUser():
    s = input("당신의 ID를 입력해주세요")

if __name__ == "__main__":
    logging.basicConfig(filename="./status.log", level=logging.DEBUG)
    parser = argparse.ArgumentParser("")
    parser.add_argument("--operationMode", required=True)
    args = parser.parse_args()
    if args == 1:
        createKey()
    elif args == 2:
        createUser()
    else:
        createBabyPicture()
        createBabyTemperature()