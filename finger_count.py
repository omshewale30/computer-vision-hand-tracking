
import cv2
import numpy as np

from sklearn.metrics import pairwise
background = None

accumulated_weight = 0.5

roi_bottom = 300
roi_top = 20
roi_left = 600
roi_right = 300


def cal_accum_weight(frame, accumulated_weight):
    
    global background
    if background is None:
        background = frame.copy().astype('float')
        return None
    
    cv2.accumulateWeighted(frame,background,accumulated_weight)
def segment(frame, threshold=25):
    diff = cv2.absdiff(background.astype('uint8'),frame)
    
    ret, thresholded = cv2.threshold(diff,threshold,255, cv2.THRESH_BINARY)
    
    contours, heirarchy = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) ==0:
        return None
    else:
        hand_segment = max(contours, key=cv2.contourArea())
        return (thresholded,hand_segment)

def count_fingers(thresholded, hand_segment):
    convex_hull = cv2.convexHull(hand_segment)
    
    top = tuple(convex_hull[convex_hull[:,:,1].argmin()[0]])
    bottom = tuple(convex_hull[convex_hull[:,:,1].argmax()[0]])
    left = tuple(convex_hull[convex_hull[:,:,0].argmin()[0]])
    right = tuple(convex_hull[convex_hull[:,:,0].argmax()[0]])
    
    cX = (left[0]+right[0]) // 2
    cY = (top[1]+bottom[1]) // 2
    
    distance = pairwise.euclidean_distances([cX,cY], Y=[left, right, top, bottom])[0]
    
    max_dist = distance.max()
    radius = int(0.9*max_dist)
    circum  = int (2*np.pi*radius)
    
    circular_roi = np.zeros(thresholded[:2],dtype='uint8')
    cv2.circle(circular_roi,(cX,cY),radius,255,10)
    
    circular_roi = cv2.bitwise_and(thresholded,thresholded,mask = circular_roi)
    contours, heirarchy = cv2.findContours(circular_roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    count = 0
    
    for cont in contours:
        (x,y,w,h) = cv2.boundingRect(cont)
        
        out_of_wrist = (cY+(0.25*cY))>(y+h)
        
        point_in_region = ((circum*0.25)>(cont.shape[0]))
        if out_of_wrist and point_in_region:
            count+=1
        
    return count

cam  = cv2.VideoCapture(0)
num_frames = 0

while True:
   print("this is being captured", cam.read())
   ret,frame = cam.read()
   frame = cv2.flip(frame, 1)
   print("this is frame", frame)

   frame_copy= frame.copy()
   
   roi = frame_copy[roi_top:roi_bottom,roi_right:roi_left]
   
   gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
   gray = cv2.GaussianBlur(gray, (7,7), 0)
   
   if num_frames<60:
       cal_accum_weight(gray,accumulated_weight)
       if num_frames<=59:
           cv2.putText(frame_copy, 'Please wait, getting the background',(200,300), cv2.FONT_HERSHEY_PLAIN, 1,(0,0,255),2)
           cv2.imshow("finger count",frame_copy)
   
   else:
       hand = segment(gray)
       
       if hand is not None:
           thresholded, hand_segment = hand
           
           cv2.drawContours(frame_copy,[hand_segment+(roi_right,roi_top)],-1,(255,0,0),5)
           
           num_fingers = count_fingers(thresholded, hand_segment)
           
           cv2.putText(frame_copy, str(num_fingers),(70,50), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255),2)
           cv2.imshow('Thresholded', thresholded)
       cv2.rectangle(frame_copy,(roi_left,roi_top),(roi_right,roi_bottom),(0,0,255),5)
       
       num_frames+=1
       cv2.imshow('Finger Count:', frame_copy)
       
       k = cv2.waitKey(1) & 0xFF
       if k == 27:
           break
   cam.release()
   cv2.destroyAllWindows()
           
