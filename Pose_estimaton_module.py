# pose estimation module 

import cv2 as cv
import mediapipe as mp
import time
import math

class poseDetector:
    def __init__(self,mode=False,upBody=False,smooth=True,detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpdraw = mp.solutions.drawing_utils
        self.mppose = mp.solutions.pose
        self.pose = self.mppose.Pose(static_image_mode=self.mode, 
                                     model_complexity=1, 
                                     smooth_landmarks=self.smooth,
                                     min_detection_confidence=self.detectionCon, 
                                     min_tracking_confidence=self.trackCon)
    
    def findPose(self,frame,draw=True):
        img_rgb = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        self.result = self.pose.process(img_rgb)
        if self.result.pose_landmarks:
           if draw:
               self.mpdraw.draw_landmarks(frame,self.result.pose_landmarks,self.mppose.POSE_CONNECTIONS)
        return frame

    def findLandmarks(self,frame,draw=True):
        self.lmlist = []
        if self.result.pose_landmarks:
            for id,lm in enumerate(self.result.pose_landmarks.landmark):
                h,w,c = frame.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                self.lmlist.append([id,cx,cy])
                if draw:
                    cv.circle(frame,(cx,cy),15,(255,0,255),-1)
        return self.lmlist

    def findAngle(self,frame,p1,p2,p3,draw=True):
        x1,y1 = self.lmlist[p1][1:]
        x2,y2 = self.lmlist[p2][1:]
        x3,y3 = self.lmlist[p3][1:]
        # calculating the angle between the lines formed by the p1 and p2 and p2 and p3
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                                math.atan2(y1 - y2, x1 - x2))
        if angle<=0:
            angle+=360
        if draw:
            cv.line(frame,(x1,y1),(x2,y2),(255,0,255),2)
            cv.line(frame,(x3,y3),(x2,y2),(255,0,255),2)
            cv.circle(frame,(x1,y1),15,(255,0,255),-1)
            cv.circle(frame,(x1,y1),15,(255,255,255),2)
            cv.circle(frame,(x2,y2),15,(255,0,255),-1)
            cv.circle(frame,(x2,y2),15,(255,255,255),2)
            cv.circle(frame,(x3,y3),15,(255,0,255),-1)
            cv.circle(frame,(x3,y3),15,(255,255,255),2)
        return angle

def main():
    ptime=0
    ctime=0
    capture = cv.VideoCapture(0)
    capture.set(3,800)
    capture.set(4,600)
    detector = poseDetector()
    while True:
        istrue,frame = capture.read()
        if not istrue:
            break
        frame = detector.findPose(frame)
        detect = detector.findLandmarks(frame,draw=False)
        detector.findAngle(frame,12,14,16)
        ctime=time.time()
        fps = 1/(ctime-ptime)
        ptime=ctime
        cv.putText(frame,f"Fps={str(int(fps))}",(30,50),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,255),2)
        cv.imshow("Webcam",frame)
        if cv.waitKey(20) & 0xff==ord('d'):
            break
    capture.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
