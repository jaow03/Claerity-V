#นำเข้าเครื่องมือที่ใช้ทั้งหมด
import cv2
import numpy as np
import time
from time import sleep

#กำหนดค่าความกว้างของกรอบของเส้น
width_min = 80 
#กำหนดค่าความสูงของกรอบของเส้น
height_min = 80 

#กำหนดอัตราการผิดพลาดที่น่าเชื่อถือ
offset= 5  

#ตำแหน่งของเส้น
pos_line_1 = 450
pos_line_2 = 650 

#ควบคุม FPS ของ Video
frame_rate= 150

#ใช้เก็บค่าของจุด X,Y
detect_1 = []
detect_2 = []

#นับจำนวนของรถที่ตรวจจับได้ในระบบ
detect_line_1 = 0
detect_line_2= 0

#ฟังก์ชันบอกจุดทีแดงที่เป็นใจกลางของกรอบ detect	
def coordinate_red_dot(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

#นำเข้าไฟล์วิดีโอ
video_ref = cv2.VideoCapture("IMG_8039.MOV")

car_cascade = cv2.CascadeClassifier("C:/Users/ACER/Desktop/detect car/Computer-Vision---Object-Detection-in-Python-master/xml files/cars.xml")

# ตรวจสอบการเคลื่อนไหวของรถ
motion_detect = cv2.createBackgroundSubtractorMOG2()

while True:
    #อ่านค่าจากวิดีโอ
    ret , frame1 = video_ref.read()
    
    #ควบคุมความเร็วของวิดีโอ
    speed = float(1/frame_rate)
    sleep(speed)
    
    #ทำภาพให้เป็นขาว-ดำ
    grey = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY) 
    #ทำให้ภาพเบลอโดยมีขนาด 5*5
    blur = cv2.GaussianBlur(grey,(5,5),5)
    #ทำภาพให้สกัดส่วนที่เคลื่อนไหว
    img_sub = motion_detect.apply(blur)
    #ทำให้ภาพขยายเป็นขนาด 5*5
    dilat = cv2.dilate(img_sub,np.ones((5,5))) 
    #ทำการสกัดขอบภายในภาพ
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatada = cv2.morphologyEx (dilat, cv2. MORPH_CLOSE , kernel)
    dilatada = cv2.morphologyEx (dilatada, cv2. MORPH_CLOSE , kernel)
    #สรุปผลลัพธ์ของการสกัดส่วนที่เคลื่อนไหว
    contorno,h=cv2.findContours(dilatada,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


    #สร้างเส้นสำหรับตรวจจับรถ เส้นที่ 1
    cv2.line(frame1, (25, pos_line_1), (1200, pos_line_1), (255,127,0), 2)
    #สร้างเส้นสำหรับตรวจจับรถ เส้นที่ 2
    cv2.line(frame1, (25, pos_line_2), (1200, pos_line_2), (255,127,0), 2)
    
    #ลูปการสร้างกรอบสำหรับใส่ให้กับวัตถุที่ตรวจจับได้
    for(i,c) in enumerate(contorno):
        (x,y,w,h) = cv2.boundingRect(c)
        validar_contorno = (w >= width_min) and (h >= height_min)
        if not validar_contorno:
            continue
        
        
        #รวมกรอบกับจุด
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)        
        coordinate = coordinate_red_dot(x, y, w, h)
        #เพิ่มค่าเข้าไปใน List detect_1
        detect_1.append(coordinate)
        #เพิ่มค่าเข้าไปใน List detect_2
        detect_2.append(coordinate)
        cv2.circle(frame1, coordinate, 4, (0, 0,255), -1)
        
        
        #เส้นตรวจจับที่ 1
        for (x,y) in detect_1:
            if y<(pos_line_1+offset) and y>(pos_line_1-offset):
                detect_line_1+=1
                cv2.line(frame1, (25, pos_line_1), (1200, pos_line_1), (0,127,255), 2)  
                detect_1.remove((x,y))
                print("Detected_1 : "+str(detect_line_1))
                #print(detect_1)
                
        #เส้นตรวจจับที่ 2
        for (x,y) in detect_2:
            if y<(pos_line_2+offset) and y>(pos_line_2-offset):
                detect_line_2+=1
                cv2.line(frame1, (25, pos_line_2), (1200, pos_line_2), (0,127,255), 2)  
                detect_2.remove((x,y))
                print("Detected_2 : "+str(detect_line_2)) 
                #print(detect_2)


    #ใส่ข้อความไปในวิดีโอ
    cv2.putText(frame1, "Line1 : "+str(detect_line_1), (250, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),4)
    cv2.putText(frame1, "Line2 : "+str(detect_line_2), (750, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),4)
    #แสดงผลลัพธ์ของวิดีโอ
    cv2.imshow("Main Video" , frame1)
    #แสดงผลลัพธ์ของวิดีโอตรวจจับ
    cv2.imshow("Detect Screen",dilatada)
    

    if cv2.waitKey(1) == 27:
        break
    
#คืนทรัพยากรให้กับระบบ    
cv2.destroyAllWindows()