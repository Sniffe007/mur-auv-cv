import pymurapi as mur
import time
import cv2
auv = mur.mur_init()
depth_j =1
import numpy as np
CLR = {
       "green":{
          "lower": (50,100,40),
          "upper" :(80,255,255)
       },
              
       "orange":{
          "lower": (10,50,50),
          "upper": (25,255,255)
       },
               
         "red":{
            "lower": (160,100,50),
            "upper":(179,255,255)
       }
 }
class PD():
    def __init__(self,P,D):
        self.P = P
        self.D=D
        self.error = 0
        self.error_p = 0
    def work(self,xj,xt,dt):
        self.error = xj-xt
        self.error_d = self.error-self.error_p
        self.error_p = self.error
        return self.P*self.error+self.D*(self.error_d)/dt
reg_depth = PD(50,0)
lower = (10,50,50)
upper = (20,255,255)

def procces_frame():
    image = auv.get_image_bottom()
    image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(image,lower,upper)
    contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    #if not contours:
     #   continue
    
    cv2.imshow('mask',mask)
    cv2.waitKey(1)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            centr,radius = cv2.minEnclosingCircle(cnt)
            circle_area = math.pi*radius**2
            
            rectangle = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rectangle)
            rectangle_area  = cv2.contourArea(np.intp(box))
            
            rect = abs(area-rectangle_area)
            circle=abs(area-circle_area)
            
            if rect>circle:
                print("Круг")
            else:
                print("Прямоугольник")
                
                
def procces_color():
    image = auv.get_image_bottom()
    image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    for color_name,bounds in CLR:
        lower = np.array(bounds["lower"])
        upper = np.array(bounds["upper"])
        
        mask = cv2.inRange(image,lower,upper)
        contours,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:
                print(color_name)
                return
                
while(True):
    depth_t=auv.get_depth()
    
   # procces_frame()
    procces_color()
    cv2.waitKey(1)
    auv.set_motor_power(2,-reg_depth.work(depth_j,depth_t,0.05))
    auv.set_motor_power(3,reg_depth.work(depth_j,depth_t,0.05))
    
    
    
        
