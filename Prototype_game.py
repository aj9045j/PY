import cv2 as cv
import mediapipe as mp
import Pose_estimaton_module as pt
import time
import random
import math

capture = cv.VideoCapture(0)

capture.set(3,1400)
capture.set(4,1100)

ctime = 0
ptime = 0  

detector = pt.poseDetector()

def get_random_position():
    x = random.randint(10,1000)
    y = random.randint(10,900)
    return x,y

game_time = time.time()
start_time = time.time()
position = get_random_position()
region = position[0]+30 , position[1]+30
count = 0
while True:
    istrue , img = capture.read()
    img = cv.flip(img,1)
    img = detector.findPose(img,draw=False)
    landms = detector.findLandmarks(img,draw=False)
    if len(landms)!=0 :
        x,y=landms[20][1],landms[20][2]
        x1,y1=landms[19][1],landms[19][2]
        distance = math.sqrt((position[0] - x) ** 2 + (position[1] - y) ** 2)
        distance2 = math.sqrt((position[0] - x1) ** 2 + (position[1] - y1) ** 2)
        cv.circle(img,(x,y),20,(255,0,255),-1)
        cv.circle(img,(x1,y1),20,(255,0,255),-1)
        if (distance<30) | (distance2<30):
            count+=1
            position = get_random_position()    
            region = position[0]+30 , position[1]+30
            start_time = time.time()  
        if time.time() - start_time >= 3:
            position = get_random_position()    
            region = position[0]+30 , position[1]+30
            start_time = time.time()  
        if time.time() - game_time >= 30:
            break
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv.circle(img,position,20,(255,255,255),-1)
    cv.putText(img,f'count:-{str(int(count))}',(900,70),cv.FONT_HERSHEY_SIMPLEX,2,(255,0,255),3)
    cv.putText(img,f'FPS:-{str(int(fps))}',(30,70),cv.FONT_HERSHEY_SIMPLEX,2,(255,0,255),3)
    cv.imshow("Frame",img)
    if cv.waitKey(1) & 0xff==ord('d') :
        break;

capture.release()
cv.destroyAllWindows()
print(count)