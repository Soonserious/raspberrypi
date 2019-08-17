import cv2, time, subprocess, picamera, socket, os, signal
from multiprocessing import Process

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


        if motionOut[-2] - 48 == 1:
            message("12")
        
    proc = subprocess.Popen(['rm', '-r', './img'])
    proc.wait()
    proc = subprocess.Popen(['mkdir', 'img'])
    proc.wait()



def message(type):
    try:
        print(sock.connect((serverIP, 5425)))

        while True:
            sock.send(bytes(type, encoding = 'utf-8'))
            print(time.time())
            rbuff =  sock.recv(1024).decode()
            print(rbuff)
            
    except:
        print("connect is unable")
    
    finally:
        print("Message is successfully send!!!")


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


#serverIP = socket.gethostbyname("jyj94.ddns.net")
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#try:
 #   print(sock.connect((serverIP, 5425)))

        
 #   sock.send(b'\x01')
 #   print(time.time())
 #   while True:
 #       rbuff =  sock.recv(1024)
 #       print(rbuff)
 #       if rbuff == b'\x22':
 #           print("connect error!")
  #          time.sleep(5)
        
  #      elif rbuff == b"\x03":
   #         p_2 = Process(target=Them)
   #         while True:    
            #p_1 = Process(target=imgprocess)
        
            #p_1.start()
    ##            print(p_2.is_alive())
      #          if p_2.is_alive() == False:
      #              p_2.start()
      #              print(p_2.is_alive())
imgprocess()
            #p_1.join()

            
#except:
#    print("connect is unable")
    




