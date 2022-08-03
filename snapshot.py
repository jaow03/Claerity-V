#  นำเข้า ไบนารีที่ต้องใช้
import cv2
import os
import time

# พาดอ่านวิดีโอ
cam = cv2.VideoCapture("IMG_8039.MOV")

try:

    # การสร้างโฟลเดอร์ที่มีชื่อข้อมูล
    if not os.path.exists('data'):
        os.makedirs('data')

    # ถ้าไม่ได้สร้างแล้วยกข้อผิดพลาด
except OSError:
    print('Error: Creating directory of data')

# frame
currentframe = 0

while (True):
    time.sleep(5) # schreenshot ทุก 5 วินาที
    
    # reading from frame
    ret, frame = cam.read()

    if ret:
        # if video is still left continue creating images
        name = './data/frame' + str(currentframe) + '.jpg'
        print('Creating...' + name)

        # writing the extracted images
        cv2.imwrite(name, frame)

        # increasing counter so that it will
        # show how many frames are created
        currentframe += 1
    else:
        break

# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()