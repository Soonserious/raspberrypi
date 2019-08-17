# To use Inference Engine backend, specify location of plugins:
# export LD_LIBRARY_PATH=/opt/intel/deeplearning_deploymenttoolkit/deployment_tools/external/mklml_lnx/lib:$LD_LIBRARY_PATH
import cv2 as cv
import numpy as np #벡터와 메트릭스에 사용되는 헤더
import argparse

def frame2_happy(point):
    if bool(point) == False :
        return False
    else :
        return True
def frame3_hp(pt):
    for ptt in pt:
        u = pt[ptt]
        if u == True:
            return "0"
    if u == False:
        return "1"

parser = argparse.ArgumentParser() #파서를 선언
parser.add_argument('--input', help='Path to image or video. Skip to capture frames from camera')#이미지 또는 비디오 경로. 카메라에서 프레임 캡처로 건너 뛰기
parser.add_argument('--thr', default=0.2, type=float, help='Threshold value for pose parts heat map')#자세 부분 히트 맵의 임계 값
parser.add_argument('--width', default=368, type=int, help='Resize input to specific width.')#특정 너비로 ​​입력 크기를 조절.
parser.add_argument('--height', default=368, type=int, help='Resize input to specific height.')#특정 높이로 ​​입력 크기를 조절.

args = parser.parse_args() #명령행 인자를 파싱하는 메소드를이용 하여 파싱

BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4, #기본 배열값
               "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
               "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
               "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }
#nose0,Reye14,Leye15,Rear16,Lear:17
POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"], #기본 배열값
               ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
               ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
               ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
               ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]

inWidth = args.width  #파싱된 너비
inHeight = args.height #파싱된 높이

net = cv.dnn.readNetFromTensorflow("/home/pi/project/human-pose-estimation-opencv-master/graph_opt.pb")#텐서플로우
#net 기본생성자
cap = cv.VideoCapture(args.input if args.input else 0) ## 카메라 킴

while cv.waitKey(1) < 0:
    hasFrame, frame = cap.read()
    if not hasFrame:
        cv.waitKey() #멈추는 방법인데 카메라가 되는이상 안멈춤
        break

    frameWidth = frame.shape[1] #카메라 배열 튜플로
    frameHeight = frame.shape[0] #위와 같음
    
    net.setInput(cv.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight), (127.5, 127.5, 127.5), swapRB=True, crop=False))#이미지에 4차원 얼룩을 만들어 이미지를 조정하여 넣음
    out = net.forward()
    out = out[:, :19, :, :]  # MobileNet output [1, 57, -1, -1], we only need the first 19 elements

    assert(len(BODY_PARTS) == out.shape[1])##에러확인

    points = [] #포인트생성
    for i in range(len(BODY_PARTS)):
        # Slice heat map of corresponging body's part.
        heatMap = out[0, i, :, :] ##dnn에서카메라 촬영을 넣어 나온 배열의19까지

        # Originally, we try to find all the local maximums. To simplify a sample
        # we just find a global one. However only a single pose at the same time
        # could be detected this way.
        _, conf, _, point = cv.minMaxLoc(heatMap)#minVal, maxVal, minLoc, maxLoc _는 값무시
        x = (frameWidth * point[0]) / out.shape[3]
        y = (frameHeight * point[1]) / out.shape[2]
        # Add a point if it's confidence is higher than threshold.
        points.append((int(x), int(y)) if conf > args.thr else None)
        #신뢰도가 임계값보다 높으면 point를 추가한다.
    for pair in POSE_PAIRS:
        partFrom = pair[0]
        partTo = pair[1]
        assert(partFrom in BODY_PARTS)
        assert(partTo in BODY_PARTS)

        idFrom = BODY_PARTS[partFrom]
        idTo = BODY_PARTS[partTo]
        # nose0,Reye14,Leye15,Rear16,Lear:17
        ap = frame2_happy(points[0])
        bp = frame2_happy(points[14])
        cp = frame2_happy(points[15])
        dp = frame2_happy(points[16])
        ep = frame2_happy(points[17])
        hp = [ap,bp,cp,dp,ep];
        

        if points[idFrom] and points[idTo]:
            cv.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
            cv.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
            cv.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
            print()


    t, _ = net.getPerfProfile()
    freq = cv.getTickFrequency() / 1000
    cv.putText(frame, '%.2fms' % (t / freq), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
    cv.imshow('OpenPose using OpenCV', frame)
    cv.destroyAllWindows()
    print(frame3_hp(hp))