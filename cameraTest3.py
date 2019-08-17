import cv2, time, subprocess, picamera, socket, os, signal
from multiprocessing import Process

####



######

proc = subprocess.Popen(['rm', '-r', './img'])
proc.wait()
proc = subprocess.Popen(['mkdir', 'img'])
proc.wait()

camera = picamera.PiCamera()

def img_save():
    imgTime = time.strftime('(%m-%d %H:%M:%S)', time.localtime(time.time()))
    imgName = "./img/" + imgTime + ".jpg"
    camera.resolution=(768, 768) #sugjjgjgasjdiofjsasljsdaflsdjifad
    camera.capture(imgName)
    return imgName

def imgprocess():
    imgName = img_save()
    print("face detection start!")
    proc_face = subprocess.Popen(["python3", "faceDetection.py", imgName], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    faceOut, faceErr = proc_face.communicate()
    if proc_face.poll() == 0:
        print("proc_face is end!")
        proc_face.kill()

    print(faceOut)
  #  print(faceOut)
    print("face detection : " + str(faceOut[-1] - 48))
    print(type(faceOut[-1]))
    if faceOut[-1]-48 == 1:
        print("face undertective!!!\nbody detective start!")
        proc_motion = subprocess.Popen(["python3", "motionDetection.py", "--input", imgName], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        motionOut, motionErr = proc_motion.communicate()
        if proc_motion.poll() == 0:
            print("proc_motion is end!")
            proc_motion.kill()
        
        print(motionOut)
        print("motion detection : ",str( motionOut[-2]-48))


        if str(motionOut[-2] - 48) == "1":
            print(type(motionOut[-2] - 48))
            message("12")
        
    proc = subprocess.Popen(['rm', '-r', './img'])
    proc.wait()
    proc = subprocess.Popen(['mkdir', 'img'])
    proc.wait()



def message(type):
    #print(sock.connect((serverIP, 5425)))
    if type == '14':
        sock.sendto(b'14', add)
    if type == '12':
        sock.sendto(b'12', add)
    


### 
def Them():
    proc = subprocess.Popen(["./raspberrypi_video"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out = proc.communicate()[0]
    out = float(out[:5])
    print(str(out))
    if out <= 37.5:
        print("1")
    else:
        print("2")
        message("14")
    time.sleep(1800)
    print("Whdamfasfdl")


### main
connectionFlag = 0
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("192.168.0.3", 5425))
add = ("jyj94.ddns.net", 5425)
sock.sendto(b"01", add)
print("send 01 to server!")   
print("send Time : ", time.time())
data, addr = sock.recvfrom(512)
print("recive", data)

if data == b'30':
    connectionFlag = 1
    print("connection is success/ starting process")

if connectionFlag == 1:
    p_2 = Process(target=Them)
    p_2.start()
    print("process is running!")
    #imgprocess()
    while True:    
        #p_1 = Process(target=imgprocess)
        imgprocess()
        #p_1.start()
        print(p_2.is_alive())
        if p_2.is_alive() == False:
            p_2.start()
            print(p_2.is_alive())
